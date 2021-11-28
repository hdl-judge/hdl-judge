from logging import Logger
from typing import Optional, List, Any, Dict, Text

from src.backend.controllers import BaseController

from src.backend.adapters.secondary.http import HTTPClient
from src.backend.adapters.secondary.database import SQLClient
from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient
from src.backend.adapters.secondary.hdl_motor import HDLMotor
from src.backend.utils.db_schema_tables import create_tables


class MainController(BaseController):

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
        self.database_client.insert_values("users", {
            "name": "admin",
            "email_address": "admin@admin.com",
            "academic_id": "000000",
            "is_professor": True,
            "is_admin": True,
            "hashed_password": "$2b$12$gHm4iwnd.8a0kalxR6ahbOejV6AeoaCgDxdOkIWdxK0HzppHQnRii"
        })
        return self.database_client.list_tables()

    def get_config(self) -> Any:
        return True

    def create_user(
        self, hashed_password: Text, name: Text, email_address: Text, academic_id: Text, is_professor: bool, is_admin: bool
    ) -> int:
        self.database_client.insert_values(
            "users",
            {
                "name": name,
                "email_address": email_address,
                "academic_id": academic_id,
                "is_professor": is_professor,
                "is_admin": is_admin,
                "hashed_password": hashed_password
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

        project_id = self.database_client.get_values("projects", "name", name)[0]["id"]

        self.database_client.insert_values(
            "projects_files",
            {
                "name": "instrucoes.txt",
                "created_by": created_by,
                "project_id": project_id,
                "default_code": ""
            }
        )

        return project_id

    def create_projects_files(
        self, name: Text, project_id: int, created_by: int, default_code: Text
    ):
        self.database_client.insert_values(
            "projects_files",
            {
                "name": name,
                "project_id": project_id,
                "created_by": created_by,
                "default_code": default_code
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
        self, name: Text, project_id: int, metadata: Text, created_by: int, code: Text
    ):
        self.database_client.insert_values(
            "submission_files",
            {
                "name": name,
                "project_id": project_id,
                "metadata": metadata,
                "created_by": created_by,
                "code": code
            }
        )
        return self.database_client.get_values("submission_files", "name", name)[0]["id"] #Corrigir dps

    def get_table_all_or_by_id(
        self, table_name: Text, id: int = None
    ) -> Dict[Text, Any]:
        return self.database_client.get_values(table_name, "id", id)

    def update_record_by_id(
        self, table_name: Text, new_values: Dict[Any, Any],id: int = None
    ) -> Dict[Text, Any]:
        return self.database_client.update_values(table_name, new_values, "id", id)

    def delete_record_by_id(
        self, table_name: Text, id: int
    ) -> Dict[Text, Any]:
        return self.database_client.delete_values(table_name, "id", id)

    def get_user_by_email(
        self, email: str = None
    ) -> Any:
        users = self.database_client.get_values("users", "email_address", email)
        if len(users) >= 1:
            return users[0]
        else:
            return None

    def get_files_to_student(self, project_id: int, user_id: int) -> List[Dict[Text, Any]]:
        files_to_return = []
        projects_files = self.database_client.get_multiple_where_values("projects_files", {"project_id": project_id})
        projects_files_names = [record["name"] for record in projects_files]

        user_submission_files = self.database_client.get_multiple_where_values("submission_files",
                                                                               {
                                                                                   "created_by": user_id,
                                                                                   "project_id": project_id
                                                                               })
        user_submission_files_project_names = [record["name"] for record in user_submission_files]

        for record in user_submission_files:
            if record["name"] in projects_files_names:
                pass
            files_to_return.append(record)

        for record in projects_files:
            if record["name"] not in user_submission_files_project_names:
                files_to_return.append({
                    "id": record["id"],
                    "project_id": record["project_id"],
                    "name": record["name"],
                    "code": record["default_code"],
                    "metadata": record.get("metadata", ""),
                    "created_at": record["created_at"],
                    "created_by": record["created_by"]
                })

        return files_to_return

    def get_projects_files(self, project_id: int) -> List[Dict[Text, Any]]:
        files_to_return = []
        projects_files = self.database_client.get_multiple_where_values("projects_files", {"project_id": project_id})

        for record in projects_files:
            files_to_return.append({
                "id": record["id"],
                "project_id": record["project_id"],
                "name": record["name"],
                "default_code": record["default_code"],
                "created_at": record["created_at"],
                "created_by": record["created_by"]
            })

        return files_to_return

    def save_submission_files(self, project_id: int, user_id: int, files: List[Dict[Text, Any]]):

        user_submission_files = self.database_client.get_multiple_where_values(
            "submission_files",
            {
                "created_by": user_id,
                "project_id": project_id,
            }
        )
        user_submission_file_names = [record["name"] for record in user_submission_files]

        for file in files:
            if file["name"] in user_submission_file_names:
                self.database_client.update_multiple_where_values(
                    "submission_files", file,
                    {"project_id": project_id, "name": file["name"], "created_by": user_id}
                )
            else:
                self.database_client.insert_values(
                    "submission_files",
                    {
                        "name": file["name"],
                        "project_id": project_id,
                        "metadata": file["metadata"],
                        "created_by": user_id,
                        "code": file["code"]
                    }
                )

    def save_project_files(self, project_id: int, user_id: int, files: List[Dict[Text, Any]]):

        project_files = self.database_client.get_multiple_where_values(
            "projects_files",
            {
                "project_id": project_id
            }
        )
        project_files_names = [record["name"] for record in project_files]

        for file in files:
            if file["name"] in project_files_names:
                self.database_client.update_multiple_where_values(
                    "projects_files", file,
                    {"project_id": project_id, "name": file["name"]}
                )
            else:
                self.database_client.insert_values(
                    "projects_files",
                    {
                        "name": file["name"],
                        "project_id": project_id,
                        "created_by": user_id,
                        "default_code": file["default_code"]
                    }
                )

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
        projects_files_names = [projects_file["name"] for projects_file in project_files_data]

        academic_id_map = {}
        user_data = self.database_client.get_values("users")
        for user in user_data:
            academic_id_map[user["id"]] = user["academic_id"]

        submission_files = self.database_client.get_values("submission_files", "project_id", project_id)

        for submission in submission_files:
            if submission["name"] in projects_files_names:
                if submission["created_by"] not in academic_id_map:
                    academic_id = f"NOT_FOUND_ACADEMIC_ID_FOR_ID{submission['created_by']}"
                    academic_id_map[submission["created_by"]] = academic_id
                else:
                    academic_id = academic_id_map[submission["created_by"]]

                student_id = submission['created_by']
                filename = f"proj{project_id}_file{submission['name']}_id{academic_id}.vhd"
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

    def get_project_submissions_by_student(self, project_id: int) -> List[Dict[Text, Any]]:
        grouped_submissions = self.database_client.get_submissions_grouped_by_user(project_id)
        return grouped_submissions
