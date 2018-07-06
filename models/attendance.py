from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer,Date,Time,Boolean,Float,TIMESTAMP,DateTime
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
    type = Column(String(20),nullable = False)
    operator_id = Column(String(10),nullable = False)

class WorkArrangementTime(Base):
    __tablename__ = 'workarrangement_type'
    typename = Column(String(20),nullable = False,primary_key = True)
    start_time = Column(Time,nullable = False)
    end_time = Column(Time, nullable = False)
    inuse = Column(Boolean,nullable = False)

class DIYGroupDivide(Base):
    __tablename__ = 'diy_group_divide'
    operator_id = Column(String(20),primary_key = True,nullable = False)
    group_parent = Column(String(50),primary_key = True,nullable = False)
    group_son = Column(String(50),primary_key = True,nullable = False)
    ids_in_son = Column(String(200),nullable = True)

class OverTime(Base):
    __tablename__ = 'overtime'
    worker_id = Column(String(20),primary_key = True,nullable = False)
    date = Column(Date,primary_key = True,nullable = False)
    start_time = Column(DateTime,nullable = False)
    end_time = Column(DateTime,nullable=False)
    hours = Column(Float,nullable=False)
    update_time = Column(TIMESTAMP)
    ratio=Column(Float,nullable=False)
    audit_state = Column(Boolean,nullable=False)
    submit_id = Column(String(20),nullable = False)
    audit_id = Column(String(20))

class Vacation(Base):
    __tablename__ ='vacation'
    worker_id = Column(String(20),primary_key = True,nullable = False)
    date = Column(Date,primary_key = True,nullable = False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    hours = Column(Float, nullable=False)
    vacation_type = Column(String(20),nullable=False)
    audit_state = Column(Boolean, nullable=False)
    submit_id = Column(String(20), nullable=False)
    audit_id = Column(String(20))

class VacationTypes(Base):
    __tablename__ = 'vacation_types'
    vacation_type=Column(String(20),nullable=False,primary_key=True)
    percent = Column(Float,nullable=False)
    frequency = Column(Integer)
    #丧假	1
# 事假	0
# 产假	1
# 休假3	0
# 婚假	1
# 工伤假	1
# 年假	1
# 病假	0.8
# 调休	0
# 陪产假	1


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    import datetime
    conn = engine.connect()
    # conn.execute("INSERT INTO vacation_types (vacation_type,percent,frequency) VALUES ('丧假','1','1'),('事假','0','9'),('产假','1','5'),('休假3','0','6'),"
    #              "('婚假','1','3'),('工伤假','1','1'),('年假','1','6'),('病假','1','7'),('调休','1','8'),('陪产假','1','4')")
    start_date=datetime.datetime.strptime('2018-01-01',"%Y-%m-%d")
    for i in range(10000):
        date=start_date+datetime.timedelta(i)
        if date.weekday()==5 or date.weekday()==6:
            mark=0
        else:
            mark=1
        conn.execute("REPLACE INTO workday (date_record,mark) VALUES ('{date_record}','{mark}')".format(date_record=datetime.datetime.strftime(date,"%Y-%m-%d"),mark=mark))
