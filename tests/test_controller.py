import pytest

from datetime import datetime

from src.backend.controllers.read_controller import MainController
from tests.mocks import logger, http_client, database_client, plagiarism_client, hdl_motor


@pytest.fixture
def controller(logger, http_client, database_client, plagiarism_client, hdl_motor):
    return MainController(logger, http_client, database_client, plagiarism_client, hdl_motor)


def test_setup_base(controller, database_client):
    database_client.list_tables.return_value = ["Table1", "Table2"]
    result = controller.setup()
    expected = ["Table1", "Table2"]
    assert result == expected


def test_create_user_base(controller, database_client):
    name = "Nome Pessoa"
    email_address =  "email@email.com"
    academic_id = "ACD123"
    is_professor = True
    is_admin = False
    hashed_password = "TEST1"
    database_client.get_values.return_value = [{
        "id": 123,
        "name": name,
        "email_address": email_address,
        "academic_id": academic_id,
        "is_professor": is_professor,
        "is_admin": is_admin,
        "hashed_password": hashed_password
    }]
    result = controller.create_user(hashed_password, name, email_address, academic_id, is_professor, is_admin)
    expected = 123
    assert result == expected


def test_create_project_base(controller, database_client):
    name = "Project"
    created_by = 13123
    database_client.get_values.return_value = [{
        "id": 124,
        "name": name,
        "created_by": created_by,
        "created_at": datetime.now(),
    }]
    result = controller.create_project(name, created_by)
    expected = 124
    assert result == expected


def test_create_projects_files_base(controller, database_client):
    name = "Project file"
    project_id = 13124
    created_by = 13125
    default_code = "CODE"
    database_client.get_values.return_value = [{
        "id": 125,
        "name": name,
        "project_id": project_id,
        "created_by": created_by,
        "default_code": default_code
    }]
    result = controller.create_projects_files(name, project_id, created_by, database_client)
    expected = 125
    assert result == expected


def test_create_testbench_files_base(controller, database_client):
    name = "tb file"
    projects_files_id = 13126
    created_by = 13127
    code = "Code Code 132 -+=code"
    database_client.get_values.return_value = [{
        "id": 126,
        "name": name,
        "projects_files_id": projects_files_id,
        "created_by": created_by,
        "code": code
    }]
    result = controller.create_testbench_files(name, projects_files_id, created_by, code)
    expected = 126
    assert result == expected


def test_get_files_to_student(controller, database_client):
    project_id = 123
    created_by = 1234
    created_at = datetime.now()

    database_client.get_multiple_where_values.side_effect = [
        [
            {
                "id": 125,
                "name": "Project file 1",
                "project_id": project_id,
                "created_by": created_by,
                "created_at": created_at,
                "default_code": "CODE_1"
            },
            {
                "id": 126,
                "name": "Project file 2",
                "project_id": project_id,
                "created_by": created_by,
                "created_at": created_at,
                "default_code": "CODE_2"
            }
        ],
        [
            {
                "id": 1235,
                "name": "Project file 2",
                "project_id": project_id,
                "metadata": "META 1",
                "code": "CODE 1",
                "created_at": created_at,
                "created_by": created_by
            },
            {
                "id": 1236,
                "name": "Project file 3",
                "project_id": project_id,
                "metadata": "META 1",
                "code": "CODE 1",
                "created_at": created_at,
                "created_by": created_by
            }
        ]
    ]

    result = controller.get_files_to_student(project_id, created_by)
    expected = [
            {
                "id": 1235,
                "name": "Project file 2",
                "project_id": project_id,
                "metadata": "META 1",
                "code": "CODE 1",
                "created_at": created_at,
                "created_by": created_by
            },
            {
                "id": 1236,
                "name": "Project file 3",
                "project_id": project_id,
                "metadata": "META 1",
                "code": "CODE 1",
                "created_at": created_at,
                "created_by": created_by
            },
            {
                "id": 125,
                "name": "Project file 1",
                "project_id": project_id,
                "metadata": "",
                "code": "CODE_1",
                "created_at": created_at,
                "created_by": created_by
            }
        ]

    assert len(result) == len(expected)
    assert result == expected
    assert database_client.get_multiple_where_values.call_count == 2


def test_save_submission_files_base(controller, database_client):
    project_id = 123
    created_by = 1234
    created_at = datetime.now()
    files = [
        {
            "id": 1235,
            "name": "Project file 1",
            "project_id": project_id,
            "metadata": "META 1-2",
            "code": "CODE 1-2",
            "created_at": created_at,
            "created_by": created_by
        },
        {
            "id": 1236,
            "name": "Project file 2",
            "project_id": project_id,
            "metadata": "META 2-2",
            "code": "CODE 2-2",
            "created_at": created_at,
            "created_by": created_by
        },
        {
            "id": 1237,
            "name": "Project file 3",
            "project_id": project_id,
            "metadata": "META 3-2",
            "code": "CODE 3-2",
            "created_at": created_at,
            "created_by": created_by
        }
    ]

    database_client.get_multiple_where_values.side_effect = [
        [
            {
                "id": 1235,
                "name": "Project file 1",
                "project_id": project_id,
                "metadata": "META 1",
                "code": "CODE 1",
                "created_at": created_at,
                "created_by": created_by
            },
            {
                "id": 1236,
                "name": "Project file 2",
                "project_id": project_id,
                "metadata": "META 2",
                "code": "CODE 2",
                "created_at": created_at,
                "created_by": created_by
            }
        ]
    ]

    result = controller.save_submission_files(project_id, created_by, files)
    assert database_client.update_multiple_where_values.call_count == 2
    assert database_client.insert_values.call_count == 1



def test_submit_all_codes_from_project_to_plagiarism_base(controller, database_client, plagiarism_client):
    projects_files_id = 137
    project_id = 547
    user_id = 12
    academic_id = "test_Academic_id"
    database_client.get_values.side_effect = [
        [{
            "id": projects_files_id,  # projects_files
            "name": "test_projects_files",
            "project_id": project_id,
            "created_at": datetime.now(),
            "created_by": user_id
        }],
        [{
            "id": 126, #submission_files
            "name": "test_submission_files",
            "projects_files_id": projects_files_id,
            "metadata": "metadata",
            "created_at": datetime.now(),
            "created_by": user_id,
            "code": "code test_submission_files"
        }],
        [{
            "id": user_id,  # users
            "name": "test_user",
            "email_address": "test@test.com",
            "academic_id": academic_id,
            "is_professor": False,
            "is_admin": False
        }]
    ]

    plagiarism_client.generate_report.return_value = ("www.test.com/123", "report as text")
    result = controller.submit_all_codes_from_project_to_plagiarism(project_id)
    expected = ("www.test.com/123", "report as text")

    assert result == expected
    assert plagiarism_client.add_student_files.call_count == 1
    assert plagiarism_client.generate_report.call_count == 1
    assert database_client.get_values.call_count == 3


def test_submit_all_codes_from_project_to_plagiarism_multiple_users_and_files(controller, database_client, plagiarism_client):
    projects_files_id = 137
    project_id = 547
    user_id = 12
    academic_id = "test_Academic_id"
    database_client.get_values.side_effect = [
        [
            {
                "id": projects_files_id,  # projects_files1
                "name": "test_projects_files1",
                "project_id": project_id,
                "created_at": datetime.now(),
                "created_by": user_id
            }
        ],
        [
            {
                "id": 126, #submission_files
                "name": "test_submission_files",
                "projects_files_id": projects_files_id,
                "metadata": "metadata",
                "created_at": datetime.now(),
                "created_by": user_id,
                "code": "code test_submission_files"
            },
            {
                "id": 127, #submission_files
                "name": "test_submission_files",
                "projects_files_id": projects_files_id+1,
                "metadata": "metadata",
                "created_at": datetime.now(),
                "created_by": user_id+1,
                "code": "code test_submission_files"
            }
        ],
        [{
            "id": user_id,  # users 1
            "name": "test_user",
            "email_address": "test@test.com",
            "academic_id": academic_id,
            "is_professor": False,
            "is_admin": False
        }],
        [{
            "id": user_id+1,  # users 2
            "name": "test_user2",
            "email_address": "test2@test.com",
            "academic_id": academic_id+"da",
            "is_professor": False,
            "is_admin": False
        }]
    ]

    plagiarism_client.generate_report.return_value = ("www.test.com/123", "report as text")
    result = controller.submit_all_codes_from_project_to_plagiarism(project_id)
    expected = ("www.test.com/123", "report as text")

    assert result == expected
    assert plagiarism_client.add_student_files.call_count == 2
    assert plagiarism_client.generate_report.call_count == 1
    assert database_client.get_values.call_count == 4


def test_submit_all_codes_from_project_to_plagiarism_less_cache_users_data_logic(controller, database_client, plagiarism_client):
    projects_files_id = 137
    project_id = 547
    user_id = 12
    academic_id = "test_Academic_id"
    database_client.get_values.side_effect = [
        [
            {
                "id": projects_files_id,  # projects_files1
                "name": "test_projects_files1",
                "project_id": project_id,
                "created_at": datetime.now(),
                "created_by": user_id
            }
        ],
        [
            {
                "id": 126, #submission_files
                "name": "test_submission_files",
                "projects_files_id": projects_files_id,
                "metadata": "metadata",
                "created_at": datetime.now(),
                "created_by": user_id,
                "code": "code test_submission_files"
            },
            {
                "id": 127, #submission_files
                "name": "test_submission_files",
                "projects_files_id": projects_files_id+1,
                "metadata": "metadata",
                "created_at": datetime.now(),
                "created_by": user_id,
                "code": "code test_submission_files"
            }
        ],
        [{
            "id": user_id,  # users
            "name": "test_user2",
            "email_address": "test2@test.com",
            "academic_id": academic_id,
            "is_professor": False,
            "is_admin": False
        }]
    ]

    plagiarism_client.generate_report.return_value = ("www.test.com/123", "report as text")
    result = controller.submit_all_codes_from_project_to_plagiarism(project_id)
    expected = ("www.test.com/123", "report as text")

    assert result == expected
    assert plagiarism_client.add_student_files.call_count == 2
    assert plagiarism_client.generate_report.call_count == 1
    assert database_client.get_values.call_count == 3


def test_get_waveform_from_submission_db_for_project_base(controller, database_client, hdl_motor):
    projects_files_id = 137
    user_id = 12
    database_client.get_multiple_where_values.side_effect = [
        [{
            "id": projects_files_id,  # projects_files
            "name": "test_projects_files",
            "project_id": 547,
            "created_at": datetime.now(),
            "created_by": user_id
        }],
        [{
            "id": 126, #submission_files
            "name": "test_submission_files",
            "projects_files_id": projects_files_id,
            "metadata": "metadata",
            "created_at": datetime.now(),
            "created_by": user_id,
            "code": "code test_submission_files"
        }],
        [{
            "id": 126, #testbench_files
            "name": "test_tb_files",
            "projects_files_id": projects_files_id,
            "created_at": datetime.now(),
            "created_by": 147,
            "code": "code test_tb_files"
        }]
    ]

    hdl_motor.get_waveform.return_value = {"status": "OK", "result": ["result"], "message": ["msg"]}
    result = controller.get_waveform_from_submission_db_for_project("toplevel_entity_test", user_id, projects_files_id)
    expected = {"status": "OK", "result": ["result"], "message": ["msg"]}

    assert result == expected
    assert hdl_motor.get_waveform.call_count == 1
    assert database_client.get_multiple_where_values.call_count == 3


def test_get_waveform_from_submission_db_for_project_multiple_files_and_ids(controller, database_client, hdl_motor):
    projects_files_id = 137
    user_id = 12
    database_client.get_multiple_where_values.side_effect = [
        [
            {
                "id": projects_files_id,  # projects_files
                "name": "test_projects_files",
                "project_id": 547,
                "created_at": datetime.now(),
                "created_by": user_id
            },
            {
                "id": projects_files_id+1,  # projects_files
                "name": "test_projects_files",
                "project_id": 547,
                "created_at": datetime.now(),
                "created_by": user_id
            }
        ],
        [{
            "id": 126, #submission_files 1
            "name": "test_submission_files1",
            "projects_files_id": projects_files_id,
            "metadata": "metadata",
            "created_at": datetime.now(),
            "created_by": user_id,
            "code": "code test_submission_files1"
        }],
        [{
            "id": 126, #testbench_files 1
            "name": "test_tb_files1",
            "projects_files_id": projects_files_id,
            "created_at": datetime.now(),
            "created_by": 147,
            "code": "code test_tb_files1"
        }],
        [
            {
                "id": 127, #submission_files 2
                "name": "test_submission_files2",
                "projects_files_id": projects_files_id+1,
                "metadata": "metadata",
                "created_at": datetime.now(),
                "created_by": user_id,
                "code": "code test_submission_files2"
            },
            {
                "id": 128,  # submission_files 3
                "name": "test_submission_files3",
                "projects_files_id": projects_files_id + 1,
                "metadata": "metadata",
                "created_at": datetime.now(),
                "created_by": user_id,
                "code": "code test_submission_files3"
            }
        ],
        [
            {
                "id": 127, #testbench_files 2
                "name": "test_tb_files2",
                "projects_files_id": projects_files_id+1,
                "created_at": datetime.now(),
                "created_by": 147,
                "code": "code test_tb_files2"
            },
            {
                "id": 128,  # testbench_files 3
                "name": "test_tb_files2",
                "projects_files_id": projects_files_id + 1,
                "created_at": datetime.now(),
                "created_by": 147,
                "code": "code test_tb_files3"
            }
        ]
    ]

    hdl_motor.get_waveform.return_value = {"status": "OK", "result": ["result"], "message": ["msg"]}
    result = controller.get_waveform_from_submission_db_for_project("toplevel_entity_test", user_id, projects_files_id)
    expected = {"status": "OK", "result": ["result"], "message": ["msg"]}

    assert result == expected
    assert hdl_motor.get_waveform.call_count == 1
    assert database_client.get_multiple_where_values.call_count == 5


def test_get_waveform_from_submission_db_for_file_base(controller, database_client, hdl_motor):
    projects_files_id = 137
    user_id = 12
    database_client.get_multiple_where_values.side_effect = [
        [{
            "id": 126, #submission_files
            "name": "test_submission_files",
            "projects_files_id": projects_files_id,
            "metadata": "metadata",
            "created_at": datetime.now(),
            "created_by": user_id,
            "code": "code test_submission_files"
        }],
        [{
            "id": 126, #testbench_files
            "name": "test_tb_files",
            "projects_files_id": projects_files_id,
            "created_at": datetime.now(),
            "created_by": 147,
            "code": "code test_tb_files"
        }]
    ]

    hdl_motor.get_waveform.return_value = {"status": "OK", "result": ["result"], "message": ["msg"]}
    result = controller.get_waveform_from_submission_db_for_file("toplevel_entity_test", user_id, projects_files_id)
    expected = {"status": "OK", "result": ["result"], "message": ["msg"]}
    assert result == expected
    assert hdl_motor.get_waveform.call_count == 1
    assert database_client.get_multiple_where_values.call_count == 2


def test_get_waveform_from_submission_db_for_file_multiple_files(controller, database_client, hdl_motor):
    projects_files_id = 137
    user_id = 12
    database_client.get_multiple_where_values.side_effect = [
        [
            {
                "id": 126, #submission_files
                "name": "test_submission_files",
                "projects_files_id": projects_files_id,
                "metadata": "metadata",
                "created_at": datetime.now(),
                "created_by": user_id,
                "code": "code test_submission_files"
            },
            {
                "id": 127,  # submission_files2
                "name": "test_submission_files2",
                "projects_files_id": projects_files_id,
                "metadata": "metadata",
                "created_at": datetime.now(),
                "created_by": user_id,
                "code": "code test_submission_files2"
            }
        ],
        [
            {
                "id": 126, #testbench_files
                "name": "test_tb_files",
                "projects_files_id": projects_files_id,
                "created_at": datetime.now(),
                "created_by": 147,
                "code": "code test_tb_files"
            },
            {
                "id": 127,  # testbench_files2
                "name": "test_tb_files2",
                "projects_files_id": projects_files_id,
                "created_at": datetime.now(),
                "created_by": 147,
                "code": "code test_tb_files2"
            }
        ]
    ]

    hdl_motor.get_waveform.return_value = {"status": "OK", "result": ["result"], "message": ["msg"]}
    result = controller.get_waveform_from_submission_db_for_file("toplevel_entity_test", user_id, projects_files_id)
    expected = {"status": "OK", "result": ["result"], "message": ["msg"]}
    assert result == expected
    assert hdl_motor.get_waveform.call_count == 1
    assert database_client.get_multiple_where_values.call_count == 2
