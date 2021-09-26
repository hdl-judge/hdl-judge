from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func


def create_tables():
   meta = MetaData()

   projects = Table(
      'projects', meta,
      Column('id', Integer, primary_key=True, autoincrement=True),
      Column('name', String),
      Column('created_at', DateTime, server_default=func.now()),
      Column('created_by', Integer),
      Column('due_time', DateTime),
   )

   projects_files = Table(
      'projects_files', meta,
      Column('id', Integer, primary_key=True, autoincrement=True),
      Column('name', String),
      Column('project_id', Integer, ForeignKey("project.id")),
      Column('created_at', DateTime, server_default=func.now()),
      Column('created_by', Integer)
   )

   testbench_files = Table(
      'testbench_files', meta,
      Column('id', Integer, primary_key=True, autoincrement=True),
      Column('name', String),
      Column('projects_files_id', Integer, ForeignKey("projects_files.id")),
      Column('created_at', DateTime, server_default=func.now()),
      Column('created_by', Integer),
      Column('code', String)
   )

   submission_files = Table(
      'submission_files', meta,
      Column('id', Integer, primary_key=True, autoincrement=True),
      Column('projects_files_id', Integer, ForeignKey("projects_files.id")),
      Column('metadata', String),
      Column('code', String),
      Column('created_at', DateTime, server_default=func.now()),
      Column('author', String),
   )

   return meta