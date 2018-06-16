from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer,Date,Time
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:0811@localhost:3306/chipsort?charset=utf8')

Base = declarative_base()

class Workday(Base):
    __tablename__ = 'workday'
    date_record = Column(Date,primary_key = True,nullable = False)
    mark = Column(Integer,nullable = False)

class WorkArrangement(Base):
    __tablename__ = 'workarrangement'
    worker_id = Column(String(20),primary_key = True,nullable = False)
    date = Column(Date,primary_key = True,nullable = False)
    type = Column(Integer,nullable = False)

class WorkArrangementTime(Base):
    __tablename__ = 'workarrangement_time'
    type = Column(Integer,nullable = False,primary_key = True)
    start_time = Column(Time,nullable = False)
    end_time = Column(Time, nullable = False)

class DIYGroupDivide(Base):
    __tablename__ = 'diy_group_divide'
    operator_id = Column(String(20),primary_key = True,nullable = False)
    group_parent = Column(String(50),primary_key = True,nullable = False)
    group_son = Column(String(50),primary_key = True,nullable = False)
    ids_in_son = Column(String(200),nullable = True)

if __name__ == '__main__':
    Base.metadata.create_all(engine)