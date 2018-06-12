from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer,Date,DateTime,Float
from sqlalchemy.orm import sessionmaker
import pymysql
engine = create_engine('mysql+pymysql://root:0811@localhost:3306/chipsort?charset=utf8')
session_class = sessionmaker(bind=engine)  # 实例和engine绑定
session = session_class()
#建立ORM类，可以通过Python类操作数据库
Base = declarative_base()

class EmployeeInservice(Base):
    __tablename__ = 'employee_inservice' # 工号	姓名	工作	组别	等级	入职日期	登记日期	离职日期
    worker_id = Column(String(10),primary_key=True)
    name = Column(String(50),nullable = False)
    dep_job = Column(String(50))
    rating = Column(Integer,default=1)
    entry_date = Column(Date)
    register_date = Column(Date,onupdate=True)

    def __repr__(self):
        return '姓名：%s，工号：%s' % (self.name,self.worker_id)

class EmployeeResigned(Base):
    __tablename__ = 'employee_resigned'
    worker_id = Column(String(10),primary_key=True)
    name = Column(String(50))
    job = Column(String(10))
    group = Column(String(50))
    rating = Column(Integer,default=1)
    entry_date = Column(Date)
    register_date = Column(Date,onupdate=True)
    resign_date = Column(Date)
    def __repr__(self):
        return '%s(%s)于%s离职' % (self.name,self.worker_id,self.resign_date)

class Events(Base):
    __tablename__ = 'events'
    number = Column(Integer,primary_key=True,autoincrement=True)
    worker_id = Column(String(10),nullable=False)
    punch_time = Column(DateTime,nullable=False)
    def __repr__(self):
        return '%s于%s打卡' % (self.worker_id,self.punch_time)

class Overtime(Base):
    __tablename__ = 'overtime'
    worker_id = Column(String(10),primary_key=True)
    date = Column(Date,primary_key=True)
    starttime = Column(DateTime,nullable=False)
    endtime = Column(DateTime,nullable=False)
    hours = Column(Float,nullable=False)
    sort = Column(Float,nullable=False)
    type = Column(String(10),nullable=False)

class Stroke(Base):
    __tablename__ = 'stroke'
    date = Column(Date,primary_key=True)
    sort = Column(Integer,nullable=False)
    def __repr__(self):
        if self.sort == 0:
            return '%s为工作日' % self.date
        elif self.sort == 1:
            return '%s为周末' % self.date
        else:
            return '%s为节假日' % self.date

class Vacation(Base):
    __tablename__='vacation'
    worker_id = Column(String(10),primary_key=True)
    date = Column(Date,primary_key=True)
    starttime = Column(DateTime,nullable=False)
    endtime = Column(DateTime,nullable=False)
    hours = Column(Float,nullable=False)
    kinds =Column(String(20))
    user = Column(String(10))
    type = Column(Integer)
    def __repr__(self):
        return '%s于%s到%s请假'%(self.worker_id,self.starttime,self.endtime)

class VacationSpecies(Base):
    __tablename__ = 'vacation_species'
    type = Column(String(10),primary_key=True)
    percent = Column(Float,nullable=False)
    def __repr__(self):
        return '休%s的工资为正常的%s' % (self.type,self.percent)

class WorkArrangement(Base):
    __tablename__ = 'workarrangement'
    worker_id = Column(String(10),primary_key = True)
    date = Column(Date,primary_key = True)
    starttime = Column(DateTime,nullable = False)
    endtime = Column(DateTime,nullable = False)
    operator_worker_id = Column(String(10))


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    old_connect = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0811',
                                  db='chipsort_old',charset='utf8')
    cursor = old_connect.cursor()
    # 获取‘chipsort_old’中的数据
    cursor.execute('SELECT * FROM employee WHERE jobs=1')  # 获取在职人员的数据
    employee_inservice_data = cursor.fetchall()
    # cursor.execute('SELECT * FROM employee WHERE job!=1')  # 获取离职人员的数据
    # employee_resigined_data = cursor.fetchall()
    # cursor.execute('SELECT * FROM events WHERE event_time>\'2018-05-01\'')  # 获取打卡时间数据
    # events_data = cursor.fetchall()
    # cursor.execute('SELECT * FROM overtime WHERE dates>\'2018-05-01\'')  # 获取加班时间数据
    # overtime_data = cursor.fetchall()
    # cursor.execute('SELECT * FROM stroke WHERE dates>\'2018-04-01\'')  # 获取工作日信息
    # stroke_data = cursor.fetchall()
    # cursor.execute('SELECT * FROM vacation_all WHERE dates>\'2018-03-01\'')  # 获取假期信息
    # vacation_data = cursor.fetchall()
    # cursor.execute('SELECT * FROM vacation_species')  # 获取假期类型数据
    # vacation_species_data = cursor.fetchall()
    # cursor.close()
    #
    # for employee_inservice in employee_inservice_data:
    #     employeeinservice = EmployeeInservice(worker_id=employee_inservice[0],name=employee_inservice[1],
    #                                           dep_job=employee_inservice[3],
    #                                           rating=employee_inservice[4],entry_date=employee_inservice[5],
    #                                           register_date=employee_inservice[6])
    #     session.add(employeeinservice)
    for i in range(1,8):
        em_in_obj = EmployeeInservice(worker_id = 's70'+str(i),name = '测试'+str(i))
        session.add(em_in_obj)
    #
    # for er in employee_resigined_data:
    #     reigned = EmployeeResigned(worker_id=er[0],name=er[1],job=er[2],group=er[3],rating=er[4],
    #                                entry_date=er[5],register_date=er[6],resign_date=er[7])
    #     session.add(reigned)
    #
    # for events in events_data:
    #     event = Events(number=events[0],worker_id=events[1],punch_time=events[2])
    #     session.add(event)
    #
    # for overtime in overtime_data:
    #     ot_obj = Overtime(worker_id=overtime[0],date=overtime[1],starttime=overtime[2],endtime=overtime[3],
    #                       hours=overtime[4],sort=overtime[5],type=overtime[6])
    #     session.add(ot_obj)
    #
    # for stroke in stroke_data:
    #     stroke_obj = Stroke(date=stroke[0],sort=stroke[1])
    #     session.add(stroke_obj)
    #
    # for vacation in vacation_data:
    #     va_obj = Vacation(worker_id=vacation[0],date=vacation[1],starttime=vacation[2],endtime=vacation[3],
    #                       hours=(vacation[3]-vacation[2]).seconds/3600,kinds=vacation[4],user=vacation[5],type=vacation[6])
    #     session.add(va_obj)
    #
    # for va_s in vacation_species_data:
    #     va_s_obj = VacationSpecies(type=va_s[0],percent=va_s[1])
    #     session.add(va_s_obj)
    #
    session.commit()