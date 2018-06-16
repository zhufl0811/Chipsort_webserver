from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OrmOperator():
    def __init__(self,Table_Class):
        self.engine = create_engine('mysql+pymysql://root:0811@localhost:3306/chipsort?charset=utf8')
        self.session_class = sessionmaker(bind=self.engine)  # 实例和engine绑定
        self.session = self.session_class()
        self.table = Table_Class
    def add_row(self,**kwargs):
        obj = self.table(**kwargs)
        self.session.add(obj)
        self.session.commit()
        self.session.close()
    def add_some_row(self,**kwargs):
        all_keys = list(kwargs.keys())
        dict_list = []
        for i in range(len(kwargs[all_keys[0]])):
            dd = {}
            for j in range(len(all_keys)):
                dd[all_keys[j]] = kwargs[all_keys[j]][i]
            dict_list.append(dd)
        for dict in dict_list:
            obj = self.table(**dict)
            self.session.add(obj)
        self.session.commit()
        self.session.close()
    def query_all(self,*args,**kwarg):
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
    def query_like(self,columnname,like):
        like_str = '%'+like+'%'
        result=self.session.query(self.table).filter(getattr(self.table,columnname).like(like_str)).all()
        return result
    def delete(self,**kwargs):
        objs = self.session.query(self.table).filter_by(**kwargs).all()
        i=0
        for obj in objs:
            self.session.delete(obj)
            i+=1
        self.session.commit()
        self.session.close()
        print('表格:%s中的%d行删除成功！'%(self.table.__tablename__,i))
    def delete_some_row(self,**kwargs):
        all_keys = list(kwargs.keys())
        dict_list = []
        for i in range(len(kwargs[all_keys[0]])):
            dd = {}
            for j in range(len(all_keys)):
                dd[all_keys[j]] = kwargs[all_keys[j]][i]
            dict_list.append(dd)
        for dict in dict_list:
            obj=self.session.query(self.table).filter_by(**dict).first()
            self.session.delete(obj)
        self.session.commit()
        self.session.close()

if __name__=='__main__':
    from models.info import EmployeeInservice
    oo_e=OrmOperator(EmployeeInservice)
    d=oo_e.query_like('dep_job','工程')
    print(d)


