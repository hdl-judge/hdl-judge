import subprocess
import os
import tempfile

from typing import Text, Dict

from src.backend.adapters.secondary.hdl_motor import HDLMotor


class GHDLMotor(HDLMotor):
    def get_waveform(self, toplevel_entity: Text, files: Dict[Text, Text]) -> Text:
        with tempfile.TemporaryDirectory() as tmpdir:
            for filename, content in files.items():
                file_path = os.path.join(tmpdir, filename)

                with open(file_path, 'w') as file:
                    file.write(content)

                output = subprocess.run(["ghdl", "-a", filename], capture_output=True, cwd=tmpdir)

            vcd_path = os.path.join(tmpdir, "result.vcd")
            subprocess.run(["ghdl", "--elab-run", toplevel_entity, "--vcd-nodate", f"--vcd={vcd_path}"], cwd=tmpdir)

            with open(vcd_path, 'r') as vcd_file:
                return vcd_file.read()
