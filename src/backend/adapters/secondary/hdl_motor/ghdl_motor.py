import base64
import subprocess
import os
import tempfile
import glob
import json

from typing import Text, List, Any, Dict
from zipfile import ZipFile

from src.backend.adapters.secondary.hdl_motor import HDLMotor

from src.backend.adapters.primary.api.schemas.submission import File
from src.backend.adapters.primary.api.schemas.submission_return import SubmissionReturn
from src.backend.adapters.primary.api.schemas.response_status import ResponseStatus


class GHDLMotor(HDLMotor):
    def get_waveform(self, files: List[File]) -> SubmissionReturn:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:

                filelist = []
                for inputFile in files:
                    content = inputFile.content
                    filename = inputFile.filename

                    (name, extension) = os.path.splitext(filename)
                    if extension not in ('.json', '.vhdl', '.vhd'):
                        continue

                    if extension == '.json':
                        json_dict = json.loads(content)
                        content = self.generate_testbench(
                            json_dict["signal"],
                            json_dict["toplevel"],
                            json_dict["clk_period"],
                        )
                        filename = f"{name}_json.vhdl"

                    with open(os.path.join(tmpdir, filename), 'w') as file:
                        file.write(content)

                    filelist.append(filename)

                # Import files in GHDL to get the entity names
                entities = []
                output = subprocess.run(["ghdl", "-i", *filelist], capture_output=True, cwd=tmpdir)
                output.check_returncode()

                with open(os.path.join(tmpdir, "work-obj93.cf"), 'r') as file:
                    for line in file:
                        if "entity" in line:
                            entities.append(line.split()[1])

                # Compilation
                for entity in entities:
                    output = subprocess.run(
                        ["ghdl", "-m", entity],
                        cwd=tmpdir,
                        capture_output=True,
                        text=True,
                    )
                    output.check_returncode()

                # Simulation
                message = ""
                for entity in entities:
                    vcd_path = os.path.join(tmpdir, f"{entity}.vcd")
                    output = subprocess.run(
                        ["ghdl", "-r", entity, f"--vcd={vcd_path}"],
                        capture_output=True,
                        cwd=tmpdir,
                        text=True,
                    )
                    output.check_returncode()
                    message += output.stdout

                vcd_paths = glob.glob(os.path.join(tmpdir, '*.vcd'))
                if len(vcd_paths) == 1:
                    with open(vcd_paths[0], 'rb') as vcd_file:
                        encoded = base64.b64encode(vcd_file.read())
                        return SubmissionReturn(status=ResponseStatus.OK,
                                                result=encoded,
                                                message=message,
                                                mimetype="",
                                                filename=os.path.basename(vcd_paths[0]))

                zip_path = os.path.join(tmpdir, "result.zip")
                with ZipFile(zip_path, 'w') as zip_file:
                    for vcd_path in vcd_paths:
                        zip_file.write(filename=vcd_path,
                                       arcname=os.path.basename(vcd_path))

                with open(zip_path, 'rb') as zip_file:
                    encoded = base64.b64encode(zip_file.read())
                    return SubmissionReturn(status=ResponseStatus.OK,
                                            result=encoded,
                                            message=message,
                                            mimetype="",
                                            filename=os.path.basename(zip_path))

        except subprocess.CalledProcessError as ex:
            return SubmissionReturn(status=ResponseStatus.ERROR, message=ex.stderr)

    def generate_testbench(self, signals: Any, toplevel_entity: Text, clk_period: int) -> Text:
        testbench = """entity {0}_json is
end {0}_json;

architecture behav of {0}_json is
    component {0}
        port ({1});
    end component;
    {2}
    for {0}_0: {0} use entity work.{0};
begin
    {0}_0: {0} port map ({3});
    process
    begin""".format(
            toplevel_entity,
            "; ".join("{0} : {1} {2}".format(s["name"], s["dir"], s["type"]) for s in signals),
            "\n    ".join("signal {0} : {1};".format(s["name"], s["type"]) for s in signals),
            ", ".join("{0} => {0}".format(s["name"]) for s in signals))

        biggest_signal = max(signals, key=lambda x: len(x["wave"]))
        last_signals = {}
        vector_signals = {}
        for s in signals:
            signal_name = s["name"]
            wave_signal = self.get_wave_signal(s, 0)
            last_signals[signal_name] = wave_signal
            if "data" in s:
                vector_signals[signal_name] = s["data"].split()

        for i in range(len(biggest_signal["wave"])):
            for s in filter(lambda signal: signal["dir"] == "in", signals):
                signal_name = s["name"]
                wave_signal = self.get_wave_signal(s, i)
                if wave_signal == '.':
                    wave_signal = last_signals[signal_name]
                elif wave_signal == '=':
                    wave_signal = vector_signals[signal_name].pop(0)
                last_signals[signal_name] = wave_signal
                testbench += "\n        {0} <= '{1}';".format(signal_name, wave_signal)

            testbench += f"\n        wait for {clk_period} ns;"

            for s in filter(lambda signal: signal["dir"] == "out", signals):
                signal_name = s["name"]
                wave_signal = self.get_wave_signal(s, i)
                if wave_signal == '.':
                    wave_signal = last_signals[signal_name]
                elif wave_signal == '=':
                    wave_signal = vector_signals[signal_name].pop(0)
                last_signals[signal_name] = wave_signal
                testbench += "\n        assert {0} = '{1}' report \"expected {0} = {1} at {2}ns\" severity error;" \
                    .format(signal_name, wave_signal, clk_period * (i + 1))

            testbench += "\n        "

        testbench += """
        assert false report "end of test" severity note;
        wait;
    end process;
end architecture;"""

        # print(testbench)

        return testbench

    @staticmethod
    def get_wave_signal(s, i):
        if i < len(s["wave"]):
            wave_signal = s["wave"][i]
        else:
            wave_signal = s["wave"][-1] if len(s["wave"]) > 0 else ""
        return wave_signal

    def run_autocorrection(self, files: List[Dict[str, Any]]) -> Text:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                filelist = []
                for inputFile in files:
                    content = inputFile['code']
                    filename = inputFile['name']
                    (name, extension) = os.path.splitext(filename)

                    if extension not in ('.vhdl', '.vhd'):
                        continue

                    with open(os.path.join(tmpdir, filename), 'w') as file:
                        file.write(content)

                    filelist.append(filename)

                # Import testbench in GHDL to get the testbench entity name
                entities = []
                output = subprocess.run(["ghdl", "-i", "testbench.vhdl"], capture_output=True, cwd=tmpdir)
                output.check_returncode()

                with open(os.path.join(tmpdir, "work-obj93.cf"), 'r') as file:
                    for line in file:
                        if "entity" in line:
                            entities.append(line.split()[1])

                # Analyse
                message = ""
                output = subprocess.run(["ghdl", "-a", *filelist], capture_output=True, cwd=tmpdir, text=True)
                output.check_returncode()
                message += output.stdout

                # Elaborate and run
                output = subprocess.run(
                    ["ghdl", "--elab-run", entities[0]],
                    capture_output=True,
                    cwd=tmpdir,
                    text=True
                )
                output.check_returncode()
                message += output.stdout

                return message

        except subprocess.CalledProcessError as ex:
            return ex.stderr
