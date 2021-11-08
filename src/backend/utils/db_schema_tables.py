from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func


def create_tables():
    meta = MetaData()

    user = Table(
        'user', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String),
        Column('email_address', String, unique=True),
        Column('academic_id', String, unique=True),
        Column('is_professor', Boolean, default=False),
        Column('is_admin', Boolean, default=False),
    )

    projects = Table(
        'projects', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String, unique=True),
        Column('created_at', DateTime, server_default=func.now()),
        Column('created_by', Integer, ForeignKey("user.id")),
        Column('due_time', DateTime),
    )

    projects_files = Table(
        'projects_files', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String, unique=True),
        Column('project_id', Integer, ForeignKey("projects.id")),
        Column('created_at', DateTime, server_default=func.now()),
        Column('created_by', Integer, ForeignKey("user.id"))
    )

    testbench_files = Table(
        'testbench_files', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String, unique=True),
        Column('projects_files_id', Integer, ForeignKey("projects_files.id")),
        Column('created_at', DateTime, server_default=func.now()),
        Column('created_by', Integer, ForeignKey("user.id")),
        Column('code', String)
    )

    submission_files = Table(
        'submission_files', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String),
        Column('projects_files_id', Integer, ForeignKey("projects_files.id")),
        Column('metadata', String),
        Column('code', String),
        Column('created_at', DateTime, server_default=func.now()),
        Column('created_by', Integer, ForeignKey("user.id")),
    )

    return meta