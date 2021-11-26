import subprocess
import os
import tempfile
import json

from typing import Text, List

from src.backend.adapters.secondary.hdl_motor import HDLMotor

from src.backend.adapters.primary.api.schemas.submission import File
from src.backend.adapters.primary.api.schemas.submission_return import SubmissionReturn
from src.backend.adapters.primary.api.schemas.response_status import ResponseStatus


class GHDLMotor(HDLMotor):
    def get_waveform(self, toplevel_entity: Text, files: List[File]) -> SubmissionReturn:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:

                filelist = []
                for inputFile in files:
                    content = inputFile.content
                    filename = inputFile.filename

                    if filename.endswith('.json'):
                        content = self.generate_testbench(content, toplevel_entity)
                        filename = f"tb.vhdl"

                    with open(os.path.join(tmpdir, filename), 'w') as file:
                        file.write(content)

                    filelist.append(filename)

                output = subprocess.run(["ghdl", "-a", *filelist], capture_output=True, cwd=tmpdir)
                output.check_returncode()

                vcd_path = os.path.join(tmpdir, "result.vcd")
                output = subprocess.run(
                    ["ghdl", "--elab-run", f"{toplevel_entity}_tb", "--vcd-nodate", f"--vcd={vcd_path}"],
                    capture_output=True,
                    cwd=tmpdir
                )
                output.check_returncode()

                with open(vcd_path, 'r') as vcd_file:
                    return SubmissionReturn(status=ResponseStatus.OK, result=vcd_file.read(), message=output.stdout)

        except subprocess.CalledProcessError as ex:
            return SubmissionReturn(status=ResponseStatus.ERROR, message=ex.stderr)

    def generate_testbench(self, content: Text, toplevel_entity: Text) -> Text:
        clk_period = 10
        signals = json.loads(content)["signal"]

        testbench = """entity {0}_tb is
end {0}_tb;

architecture behav of {0}_tb is
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
        for i in range(len(biggest_signal["wave"])):
            testbench += """
        {0}
        wait for {1} ns;
        {2}""".format(
                "\n        ".join(
                    "{0} <= '{1}';".format(s["name"], s["wave"][i]) for s in signals if s["dir"] == "in"),
                clk_period,
                "\n        ".join("assert {0} = '{1}' report \"expected {0} = {1} at {2}ns\" severity error;".format(
                    s["name"],
                    s["wave"][i],
                    clk_period * (i + 1)
                ) for s in signals if s["dir"] == "out")
            )

        testbench += """
        assert false report "end of test" severity note;
        wait;
    end process;
end architecture;"""

        return testbench
