import tornado.web
from handlers.basehandler import BaseHandler
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import db

engine = create_engine('mysql+pymysql://root:0811@localhost:3306/chipsort?charset=utf8')
session_class = sessionmaker(bind = engine)  # 实例和engine绑定
session = session_class()

class WorkArrangementHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        worker_id = self.get_secure_cookie('worker_id')
        worker_info=session.query(db.EmployeeInservice).filter_by(worker_id=worker_id).first()
        name = worker_info.name
        dep_job = worker_info.dep_job
        dep_job_members = session.query(db.EmployeeInservice).filter_by(dep_job=dep_job).all()
        print(len(dep_job_members))
        self.render('attendance/workarrangement.html',name=name,worker_id=worker_id,dep_job=dep_job,dep_job_members=dep_job_members)

    def post(self):

        # id_be_arrangement = self.get_argument('id_be_arrangement')
        # worker_ids = id_be_arrangement.split(',')
        # startdate = datetime.datetime.strptime(self.get_argument('startdate'),'%Y-%m-%d')
        # enddate = datetime.datetime.strptime(self.get_argument('enddate'),'%Y-%m-%d')
        # days = (enddate-startdate).days
        # starttime_get = self.get_argument('starttime')
        # endtime_get = self.get_argument('endtime')
        # for i in range(days):
        #     for id in worker_ids:
        #         date = startdate + datetime.timedelta(i)
        #         starttime = datetime.datetime.strptime(str(date)+ starttime_get,'%Y-%m-%d %H:%M')
        #         endtime = datetime.datetime.strptime(str(date) + endtime_get,'%Y-%m-%d %H:%M')
        #         print(starttime)
        #         work_arrangement_obj = db.WorkArrangement(worker_id=id,
        #                                                   date=date,
        #                                                   starttime=starttime,
        #                                                   endtime=endtime)
        #         session.add(work_arrangement_obj)
        session.commit()
        self.write('成功')
