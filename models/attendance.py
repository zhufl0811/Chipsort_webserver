from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer,Date
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:0811@localhost:3306/chipsort?charset=utf8')

Base = declarative_base()

class Workday(Base):
    __tablename__ = 'workday'
    date_record = Column(Date,primary_key = True,nullable = False)
    mark = Column(Integer,nullable = False)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
