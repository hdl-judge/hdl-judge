import subprocess
import os
import tempfile

from typing import Text, List

from src.backend.adapters.secondary.hdl_motor import HDLMotor

from src.backend.adapters.primary.api.schemas.submission import File
from src.backend.adapters.primary.api.schemas.submission_return import SubmissionReturn
from src.backend.adapters.primary.api.schemas.response_status import ResponseStatus


class GHDLMotor(HDLMotor):
    def get_waveform(self, toplevel_entity: Text, files: List[File]) -> SubmissionReturn:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                for inputFile in files:
                    file_path = os.path.join(tmpdir, inputFile.filename)

                    with open(file_path, 'w') as file:
                        file.write(inputFile.content)

                    output = subprocess.run(["ghdl", "-a", inputFile.filename], capture_output=True, cwd=tmpdir)
                    output.check_returncode()

                vcd_path = os.path.join(tmpdir, "result.vcd")
                output = subprocess.run(
                    ["ghdl", "--elab-run", toplevel_entity, "--vcd-nodate", f"--vcd={vcd_path}"],
                    capture_output=True,
                    cwd=tmpdir
                )
                output.check_returncode()

                with open(vcd_path, 'r') as vcd_file:
                    return SubmissionReturn(status=ResponseStatus.OK, result=vcd_file.read(), message=output.stdout)

        except subprocess.CalledProcessError as ex:
            return SubmissionReturn(status=ResponseStatus.ERROR, message=ex.stderr)

