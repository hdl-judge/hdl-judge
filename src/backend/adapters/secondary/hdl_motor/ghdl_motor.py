import subprocess
import os
import tempfile

from typing import Text, List

from src.backend.adapters.secondary.hdl_motor import HDLMotor

from src.backend.adapters.primary.api.schemas.submission import File


class GHDLMotor(HDLMotor):
    def get_waveform(self, toplevel_entity: Text, files: List[File]) -> Text:
        with tempfile.TemporaryDirectory() as tmpdir:
            for inputFile in files:
                file_path = os.path.join(tmpdir, inputFile.filename)

                with open(file_path, 'w') as file:
                    file.write(inputFile.content)

                output = subprocess.run(["ghdl", "-a", inputFile.filename], capture_output=True, cwd=tmpdir)

            vcd_path = os.path.join(tmpdir, "result.vcd")
            subprocess.run(["ghdl", "--elab-run", toplevel_entity, "--vcd-nodate", f"--vcd={vcd_path}"], cwd=tmpdir)

            with open(vcd_path, 'r') as vcd_file:
                return vcd_file.read()
