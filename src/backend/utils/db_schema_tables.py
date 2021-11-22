from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func


def create_tables():
    meta = MetaData()

    users = Table(
        'users', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('email_address', String, unique=True),
        Column('academic_id', String, unique=True),
        Column('is_professor', Boolean, default=False),
        Column('is_admin', Boolean, default=False),
        Column('hashed_password', String)
    )

    projects = Table(
        'projects', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String, unique=True),
        Column('created_at', DateTime, server_default=func.now()),
        Column('created_by', Integer, ForeignKey("users.id")),

    )

    projects_files = Table(
        'projects_files', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('project_id', Integer, ForeignKey("projects.id", onupdate="CASCADE", ondelete="CASCADE")),
        Column('created_at', DateTime, server_default=func.now()),
        Column('created_by', Integer, ForeignKey("users.id")),
        Column('default_code', String)
    )

    testbench_files = Table(
        'testbench_files', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String, unique=True),
        Column('projects_files_id', Integer, ForeignKey("projects_files.id")),
        Column('created_at', DateTime, server_default=func.now()),
        Column('created_by', Integer, ForeignKey("users.id")),
        Column('code', String)
    )

    submission_files = Table(
        'submission_files', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('project_id', Integer, ForeignKey("projects.id", onupdate="CASCADE", ondelete="CASCADE")),
        Column('metadata', String),
        Column('code', String),
        Column('created_at', DateTime, server_default=func.now()),
        Column('created_by', Integer, ForeignKey("users.id")),
    )

    return meta
