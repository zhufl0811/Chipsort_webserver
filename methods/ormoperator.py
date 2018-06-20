from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

Base = declarative_base()

class OrmOperator():
    def __init__(self,Table_Class):
        self.engine = create_engine('mysql+pymysql://root:0811@localhost:3306/chipsort?charset=utf8')
        self.session_class = sessionmaker(bind=self.engine)  # 实例和engine绑定
        self.session = self.session_class()
        self.table = Table_Class
    def add_row(self,**kwargs): #在表中增加1行的方法，用法为object.addrow(column1='***',column2='***')
        obj = self.table(**kwargs)
        self.session.add(obj)
        self.session.commit()
        self.session.close()
    def add_some_row(self,**kwargs):
        #增加多行的方法，用法为object.add_some_row(column1=[1,2,3,4],column2=[a,b,c,d]),
        # 其中1234和abcd一一对应
        all_keys = list(kwargs.keys())
        dict_list = []
        for i in range(len(kwargs[all_keys[0]])):
            dd = {}
            for j in range(len(all_keys)):
                dd[all_keys[j]] = kwargs[all_keys[j]][i]
            dict_list.append(dd)
        conn=self.engine.connect()
        conn.execute(self.table.__table__.insert(),dict_list)
        # for dict in dict_list:
        #     obj = self.table(**dict)
        #     self.session.add(obj)
        # self.session.commit()
        # self.session.close()
    def query_all(self,*args,**kwarg):
        #查询方法，Object.query_all(‘要返回的列1’...,column1='xxx',column2='ddd'),
        # 如果arg中没有值，则返回查询到的对象
        #如果arg有一个值，则返回这一列数据的列表
        #如果arg中多于一个值，则返回一个字典（key为列名）
        if args:
            if len(args)==1:
                col = args[0]
                result = []
                data = self.session.query(getattr(self.table, col)).filter_by(**kwarg).all()
                for item in data:
                    result.append(item[0])
                self.session.close()
                return result
            else:
                result_dict={}
                for arg in args:
                    result = []
                    data = self.session.query(getattr(self.table, arg)).filter_by(**kwarg).all()
                    for item in data:
                        result.append(item[0])
                    result_dict[arg]=result
                self.session.close()
                return result_dict
        else:
            result=self.session.query(self.table).filter_by(**kwarg).all()
            self.session.close()
            return result
    def query_like(self,columnname,like):#模糊查询
        like_str = '%'+like+'%'
        result=self.session.query(self.table).filter(getattr(self.table,columnname).like(like_str)).all()
        return result
    def delete(self,**kwargs):#删除数据
        objs = self.session.query(self.table).filter_by(**kwargs).all()
        i=0
        for obj in objs:
            self.session.delete(obj)
            i+=1
        self.session.commit()
        self.session.close()
        print('表格:%s中的%d行删除成功！'%(self.table.__tablename__,i))
    def delete_some_row(self,**kwargs):#删除多行数据，用法类似add_some_row
        all_keys = list(kwargs.keys())
        dict_list = []
        for i in range(len(kwargs[all_keys[0]])):
            dd = {}
            for j in range(len(all_keys)):
                dd[all_keys[j]] = kwargs[all_keys[j]][i]
            dict_list.append(dd)
        conn = self.engine.connect()
        conn.execute(self.table.__table__.delete(),dict_list)
        # for dict in dict_list:
        #     obj=self.session.query(self.table).filter_by(**dict).first()
        #     if obj:
        #         self.session.delete(obj)
        # self.session.commit()
        # self.session.close()

if __name__=='__main__':
    from models.attendance import DIYGroupDivide
    oo_e=OrmOperator(DIYGroupDivide)
    oo_e.add_row(operator_id='s123',
                 group_parent='生产|包装',
                 group_son='A',
                 ids_in_son='s135,s178,s198')


