from logging import Logger
from typing import Optional, List, Any, Dict, Text

from src.backend.controllers import BaseController

from src.backend.adapters.secondary.http import HTTPClient
from src.backend.adapters.secondary.database import SQLClient
from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient
from src.backend.adapters.secondary.hdl_motor import HDLMotor
from src.backend.utils.db_schema_tables import create_tables


class MainController(BaseController):
    @property
    def POSTS_ENDPOINT(self):
        return "https://www.uol.com.br/"

    def __init__(
            self,
            logger: Logger = None,
            http_adapter: HTTPClient = None,
            database_client: SQLClient = None,
            plagiarism_client: PlagiarismDetectorClient = None,
            code_motor: HDLMotor = None
    ):
        super().__init__(logger)
        self.http_adapter = http_adapter
        self.database_client = database_client
        self.plagiarism_client = plagiarism_client
        self.code_motor = code_motor

    def get_data(self) -> Dict[Text, Any]:
        result = self.http_adapter.get(self.POSTS_ENDPOINT)
        return result

    def submit_codes_to_plagiarism(self):
        file = open("C:\\Users\\felip\\Documents\\GitHub\\hdl-judge\\test_moss\\subs\\F_POLI-1.vhd", 'r')
        code = file.read()
        file.close()

        # self.plagiarism_client.add_base_file({"test1.vhd": code})
        self.plagiarism_client.add_student_files(1, {"test1.vhd": code})
        self.plagiarism_client.add_student_files(2, {"test2.vhd": code})
        self.plagiarism_client.add_student_files(3, {"test3.vhd": code})
        url, report_as_text = self.plagiarism_client.generate_report()
        self.plagiarism_client.clean()
        return url

    def setup(self):
        # Database setup
        metadata = create_tables()
        self.database_client.create_table(metadata)
        return self.database_client.list_tables()

    def get_config(self) -> Any:
        return True

    def create_user(
        self, name: Text, email_address: Text, academic_id: Text, is_professor: bool, is_admin: bool
    ) -> int:
        self.database_client.insert_values(
            "users",
            {
                "name": name,
                "email_address": email_address,
                "academic_id": academic_id,
                "is_professor": is_professor,
                "is_admin": is_admin
            }
        )
        return self.database_client.get_values("users", "email_address", email_address)[0]["id"]

    def create_project(
        self, name: Text, created_by: int
    ):
        self.database_client.insert_values(
            "projects",
            {
                "name": name,
                "created_by": created_by
            }
        )
        return self.database_client.get_values("projects", "name", name)[0]["id"]

    def create_projects_files(
        self, name: Text, project_id: int, created_by: int
    ):
        self.database_client.insert_values(
            "projects_files",
            {
                "name": name,
                "project_id": project_id,
                "created_by": created_by
            }
        )
        return self.database_client.get_values("projects_files", "name", name)[0]["id"]

    def create_testbench_files(
        self, name: Text, projects_files_id: int, created_by: int, code: Text
    ) -> int:
        self.database_client.insert_values(
            "testbench_files",
            {
                "name": name,
                "projects_files_id": projects_files_id,
                "created_by": created_by,
                "code": code
            }
        )
        return self.database_client.get_values("testbench_files", "name", name)[0]["id"]

    def create_submission_files(
        self, name: Text, projects_files_id: int, metadata: Text, created_by: int, code: Text
    ):
        self.database_client.insert_values(
            "submission_files",
            {
                "name": name,
                "projects_files_id": projects_files_id,
                "metadata": metadata,
                "created_by": created_by,
                "code": code
            }
        )
        return self.database_client.get_values("submission_files", "name", name)["id"] #Corrigir dps

    def get_table_all_or_by_id(
        self, table_name: Text, id: int = None
    ) -> Dict[Text, Any]:
        return self.database_client.get_values(table_name, "id", id)

    def delete_record_by_id(
        self, table_name: Text, id: int
    ) -> Dict[Text, Any]:
        return self.database_client.delete_values(table_name, "id", id)

    def submit_all_codes_from_one_file_to_plagiarism(
        self, projects_files_id: int
    ):
        submission_files = self.database_client.get_files("submission_files", "projects_files_id", projects_files_id)

        for submission in submission_files:
            academic_id = self.database_client.get_files("user", "id", submission["created_by"])["academic_id"]
            student_id = submission['created_by']
            filename = f"file{projects_files_id}_id{academic_id}.vhd"
            code = submission["code"]
            self.plagiarism_client.add_student_files(student_id, {filename: code})

        url, report_as_text = self.plagiarism_client.generate_report()
        self.plagiarism_client.clean()
        return url, report_as_text

    def submit_all_codes_from_project_to_plagiarism(
        self, project_id: int
    ):
        project_files_data = self.database_client.get_values("projects_files", "project_id", project_id)
        academic_id_map = {}
        for projects_file in project_files_data:
            projects_files_id = projects_file["id"]
            submission_files = self.database_client.get_values("submission_files", "projects_files_id", projects_files_id)

            for submission in submission_files:
                if submission["created_by"] not in academic_id_map:
                    academic_id = self.database_client.get_values("user", "id", submission["created_by"])[0]["academic_id"]
                    academic_id_map[submission["created_by"]] = academic_id
                else:
                    academic_id = academic_id_map[submission["created_by"]]

                student_id = submission['created_by']
                filename = f"proj{project_id}_file{projects_files_id}_id{academic_id}.vhd"
                code = submission["code"]
                self.plagiarism_client.add_student_files(student_id, {filename: code})

        url, report_as_text = self.plagiarism_client.generate_report()
        self.plagiarism_client.clean()
        return url, report_as_text

    def get_waveform_from_submission(
        self, toplevel_entity: Text, files: List[Any] #List[File]
    ) -> Dict[Text, Any]:
        return self.code_motor.get_waveform(toplevel_entity, files)

    def get_waveform_from_submission_db_for_project(
        self, toplevel_entity: Text, user_id: int, project_id: int
    ) -> Dict[Text, Any]:
        files = []
        list_projects_files_ids = self.database_client.get_multiple_where_values('projects_files', {
                                                                        "project_id": project_id
                                                                    })

        for projects_files_id in [val['id'] for val in list_projects_files_ids]:

            user_files = self.database_client.get_multiple_where_values('submission_files', {
                                                                            "created_by": user_id,
                                                                            "projects_files_id": projects_files_id
                                                                        })
            tb_files = self.database_client.get_multiple_where_values('testbench_files', {
                                                                          "projects_files_id": projects_files_id
                                                                      })
            files.extend([{
                "content": user_f["code"],
                "filename": f"file_{project_id}_{projects_files_id}_{user_id}"
            } for user_f in user_files])
            files.extend([{
                "content": tb_f["code"],
                "filename": f"tb_{project_id}_{projects_files_id}"
            } for tb_f in tb_files])
        return self.code_motor.get_waveform(toplevel_entity, files)

    def get_waveform_from_submission_db_for_file(
        self, toplevel_entity: Text, user_id: int, projects_files_id: int
    ) -> Dict[Text, Any]:
        files = []
        user_files = self.database_client.get_multiple_where_values('submission_files',
                                                                    {
                                                                        "created_by": user_id,
                                                                        "projects_files_id": projects_files_id
                                                                    })
        tb_files = self.database_client.get_multiple_where_values('testbench_files',
                                                                  {
                                                                      "projects_files_id": projects_files_id
                                                                  })
        files.extend([{
            "content": val["code"],
            "filename": f"file_{projects_files_id}_{user_id}"
        } for val in user_files])
        files.extend([{
            "content": val["code"],
            "filename": f"tb_{projects_files_id}"
        } for val in tb_files])

        return self.code_motor.get_waveform(toplevel_entity, files)
