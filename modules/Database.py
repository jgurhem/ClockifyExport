from datetime import date
from typing import Tuple
from modules.Entry import Entry as EntryData

from sqlalchemy import (
    Column,
    Integer,
    Select,
    String,
    ForeignKey,
    Boolean,
    Table,
    create_engine,
    DateTime,
    Date,
    select,
    or_,
    and_,
    not_
)
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import sum

from modules.TaskTime import TaskTime

Base = declarative_base()

entry_tag = Table(
    "entry_tag",
    Base.metadata,
    Column("entry_id", Integer, ForeignKey("entry.entry_id")),
    Column("tag_id", Integer, ForeignKey("tag.tag_id")),
)


class Entry(Base):
    __tablename__ = "entry"
    entry_id = Column(Integer, primary_key=True)
    id = Column(String, unique=True)
    description = Column(String)
    billable = Column(Boolean)
    ignore = Column(Boolean)
    project_id = Column(Integer, ForeignKey("project.project_id"), nullable=False)
    project = relationship("Project", backref=backref("project"))
    end_datetime = Column(DateTime)
    start_datetime = Column(DateTime)
    start_date = Column(Date)
    duration = Column(Integer)
    task_id = Column(Integer, ForeignKey("task.task_id"))
    task = relationship("Task", backref=backref("task"))
    tags = relationship("Tag", secondary=entry_tag, backref=backref("tag"))


class Tag(Base):
    __tablename__ = "tag"
    tag_id = Column(Integer, primary_key=True)
    name = Column(String)


class Project(Base):
    __tablename__ = "project"
    project_id = Column(Integer, primary_key=True)
    name = Column(String)


class Task(Base):
    __tablename__ = "task"
    task_id = Column(Integer, primary_key=True)
    name = Column(String)
    id = Column(String)


class Database:
    def __init__(self) -> None:
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def add_entry(self, entry: EntryData) -> None:
        # check if entry exists
        entry_db = self.session.query(Entry).filter(Entry.id == entry.id).one_or_none()
        if not entry_db:
            entry_db = Entry(
                id=entry.id,
                description=entry.description,
                billable=entry.billable,
                end_datetime=entry.enddate,
                start_datetime=entry.startdate,
                start_date=entry.startdate.date(),
                duration=entry.duration.total_seconds(),
            )

        project = (
            self.session.query(Project)
            .filter(Project.name == entry.project)
            .one_or_none()
        )
        if not project:
            project = Project(name=entry.project)
            self.session.add(project)
        entry_db.project = project

        if entry.task_name != "":
            task = (
                self.session.query(Task).filter(Task.id == entry.task_id).one_or_none()
            )
            if not task:
                task = Task(id=entry.task_id, name=entry.task_name)
                self.session.add(task)
            entry_db.task = task

        for t in entry.tags:
            tag = self.session.query(Tag).filter(Tag.name == t).one_or_none()
            if not tag:
                tag = Tag(name=t)
                self.session.add(tag)
            entry_db.tags.append(tag)
        entry_db.ignore = "Ignore" in entry.tags

        self.session.add(entry_db)

    def finalize(self):
        self.session.commit()

    def __create_clause(tp: str):
        s = tp.split("___")
        if len(s) == 1:
            return and_(Project.name == s[0])
        else:
            return and_(Project.name == s[0], Task.name == s[1])

    def __ignore_clause(stmt: Select[Tuple[str, str, date, int]], ignore:list[str]):
        if len(ignore) == 0:
            return stmt
        else:
            return stmt.where(not_(or_(*[Database.__create_clause(i) for i in ignore])))


    def list_projects_tasks_time(self, start, end, ignore:list[str], include_ignored=False, include_not_billable=False) -> list[TaskTime]:
        stmt = select(Project.name, Task.name, Entry.start_date, sum(Entry.duration))
        if not include_ignored:
            stmt = stmt.where(Entry.ignore == False)
        if not include_not_billable:
            stmt = stmt.where(Entry.billable == True)
        stmt = (
            stmt.where(Entry.start_datetime >= start)
            .where(Entry.end_datetime <= end)
            .join(Entry.task, full=True)
            .join(Entry.project)
            .group_by(Entry.start_date, Project.name, Task.name)
        )
        stmt = Database.__ignore_clause(stmt, ignore)

        return [TaskTime(result[0], result[1], result[2], result[3]) for result in self.session.execute(stmt)]

    def list_day_total(self, start, end, ignore:list[str], include_ignored=False, include_not_billable=False) -> list[TaskTime]:
        stmt = select(Entry.start_date, sum(Entry.duration))
        if not include_ignored:
            stmt = stmt.where(Entry.ignore == False)
        if not include_not_billable:
            stmt = stmt.where(Entry.billable == True)
        stmt = (
            stmt.where(Entry.start_datetime >= start)
            .where(Entry.end_datetime <= end)
            .join(Entry.task, full=True)
            .join(Entry.project)
            .group_by(Entry.start_date)
        )
        stmt = Database.__ignore_clause(stmt, ignore)

        return [TaskTime(None, None, result[0], result[1]) for result in self.session.execute(stmt)]
