from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer,Date
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:0811@localhost:3306/chipsort?charset=utf8')

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    worker_id = Column(String(10),primary_key = True)
    psd = Column(String(50),nullable = False)
    register_date = Column(Date, onupdate = True)
    manage_groups = Column(String(200))
    def __repr__(self):
        return '工号：%s,注册时间：%s' % (self.worker_id,self.register_date)

class Role(Base):
    __tablename__ = 'role'
    role_name = Column(String(30),primary_key = True)
    description = Column(String(100))
    def __repr__(self):
        return (self.role_name+':'+self.description)

class Permission(Base):
    __tablename__ = 'permission'
    url = Column(String(120),primary_key = True)
    description = Column(String(100))
    def __repr__(self):
        return (self.url+':'+self.description)

class UserRole(Base):
    __tablename__ = 'user_role'
    id = Column(Integer,primary_key = True,autoincrement = True)
    worker_id = Column(String(10),nullable = False)
    role_name = Column(String(30))
    def __repr__(self):
        return '工号：%s的角色为：%s' % (self.worker_id,self.role_name)


class RolePermission(Base):
    __tablename__ = 'role_permission'
    id = Column(Integer,primary_key = True)
    role_name = Column(String(30),nullable = False)
    url = Column(String(120))
    def __repr__(self):
        return '角色:%s可以访问%s'%(self.role_name,self.url)

if __name__ == '__main__':
    Base.metadata.create_all(engine)


