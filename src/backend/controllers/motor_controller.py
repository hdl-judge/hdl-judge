from logging import Logger

from src.backend.controllers import BaseController

from src.backend.adapters.secondary.database import SQLClient
from src.backend.adapters.secondary.hdl_motor import HDLMotor
from src.backend.adapters.primary.api.schemas.submission import File


class MotorController(BaseController):
    def __init__(
            self,
            logger: Logger = None,
            database_client: SQLClient = None,
            code_motor: HDLMotor = None
    ):
        super().__init__(logger)
        self.database_client = database_client
        self.code_motor = code_motor

    def submit_codes_to_run(self, project_id: int, user_id: int, is_admin: bool):
        db_files = self.database_client.get_multiple_where_values(
            'projects_files' if is_admin else 'submission_files',
            {
                'project_id': project_id,
                'created_by': user_id,
            }
        )

        files = []
        for record in db_files:
            new_file = File(filename=record['name'], content=record['default_code' if is_admin else 'code'])
            files.append(new_file)

        return self.code_motor.get_waveform(files)

    def run_autocorrection(self, project_id: int):
        rows = self.database_client.get_multiple_where_values(
            'submission_files',
            {
                'project_id': project_id,
            }
        )

        testbenches = self.database_client.get_values('testbench_files', 'project_id', project_id)
        if len(testbenches) < 1:
            return
        testbench = testbenches[0]

        files_grouped_by_user = {}
        for row in rows:
            if row['created_by'] not in files_grouped_by_user:
                files_grouped_by_user[row['created_by']] = []

            files_grouped_by_user[row['created_by']].append(row)

        messages = {}
        for user_id, files in files_grouped_by_user.items():
            files.append(testbench)
            messages[user_id] = self.code_motor.run_autocorrection(files)

        return messages
