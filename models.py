from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table, CheckConstraint
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'
    pk_id = Column(Integer, primary_key=True)
    group_name = Column(String(5), nullable=False)


class Students(Base):
    __tablename__ = 'students'
    pk_id = Column(Integer, primary_key=True)
    student_name = Column(String(30), nullable=False)
    fk_group_id = Column(Integer, ForeignKey(Groups.pk_id, ondelete='CASCADE'), nullable=False)


class Teachers(Base):
    __tablename__ = 'teachers'
    pk_id = Column(Integer, primary_key=True)
    teacher_name = Column(String(30), nullable=False)


class Subjects(Base):
    __tablename__ = 'subjects'
    pk_id = Column(Integer, primary_key=True)
    subject_name = Column(String(30), nullable=False)
    fk_teacher_id = Column(Integer, ForeignKey(Teachers.pk_id, ondelete='CASCADE'), nullable=False)


class Marks(Base):
    __tablename__ = 'marks'
    pk_id = Column(Integer, primary_key=True)
    mark_value = Column(Integer, CheckConstraint('mark_value >= 0 AND mark_value <= 100'), nullable=False)
    mark_date = Column(DateTime, nullable=False, default=datetime.now())
    fk_subject_id = Column(Integer, ForeignKey(Subjects.pk_id, ondelete='CASCADE'), nullable=False)
    fk_student_id = Column(Integer, ForeignKey(Students.pk_id, ondelete='CASCADE'), nullable=False)



