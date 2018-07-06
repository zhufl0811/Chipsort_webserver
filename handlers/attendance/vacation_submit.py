import tornado.web
from ..basehandler import BaseHandler
from models.auth import UserRole
from models.info import EmployeeInservice
from models.attendance import WorkArrangementTime,WorkArrangement,VacationTypes,Workday
import re, datetime

class VacationSubmitHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        push_data={
            'worker_id':self.worker_id,
            'id_name':self.id_name,
            'id_group':self.id_group,
            'ids_can_operate':[],
            'groups':[],
            'work_type_time':{},
            'vacation_types':[]
        }
        role_of_this_id=[rolename[0] for rolename in self.session.query(UserRole.role_name).filter(UserRole.worker_id==self.worker_id).all()]
        if ('人事' in role_of_this_id or 'admin' in role_of_this_id):
            push_data['ids_can_operate']=[id[0] for id in self.session.query(EmployeeInservice.worker_id).all()]
            push_data['groups']=list(set([group[0] for group in self.session.query(EmployeeInservice.dep_job).all()]))
        else:
            group_of_this_id=self.session.query(EmployeeInservice.dep_job).filter(EmployeeInservice.worker_id==self.worker_id).first()[0]
            if group_of_this_id[-2:]=='经理':
                push_data['ids_can_operate']=[id[0] for id in self.session.query(EmployeeInservice.worker_id).filter(EmployeeInservice.dep_job.like('%'+group_of_this_id[:2]+'%')).all()]
                try:
                    push_data['ids_can_operate'].remove(self.worker_id.lower())
                except:
                    push_data['ids_can_operate'].remove(self.worker_id.upper())
                push_data['groups']=list(set([group[0] for group in self.session.query(EmployeeInservice.dep_job).filter(EmployeeInservice.dep_job.like('%'+group_of_this_id[:2]+'%')).all()]))
                push_data['groups'].remove(group_of_this_id)
            else:
                push_data['ids_can_operate']=[id[0] for id in self.session.query(EmployeeInservice.worker_id).filter(EmployeeInservice.dep_job==group_of_this_id).all()]
                push_data['groups']=[group_of_this_id]
        push_data['groups'].append('全部')
        work_type_objs=self.session.query(WorkArrangementTime).all()
        for obj in work_type_objs:
            push_data['work_type_time'][obj.typename]=[str(obj.start_time)[:-3],str(obj.end_time)[:-3]]
        push_data['vacation_types']=[type[0] for type in self.session.query(VacationTypes.vacation_type).order_by(VacationTypes.frequency.desc()).all()]
        self.finish(push_data)
    def post(self):
        post_info=str(self.request.body,encoding='utf-8')[1:-1]
        if 'start_date' in post_info:
            post_info=post_info.replace('\"','')
            ids_want_vacation = re.search("ids:\[(.*)\]", post_info).groups()[0].split(',')
            start_date = re.search("start_date:(\d\d\d\d-\d\d-\d\d)", post_info).groups()[0]
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = re.search("end_date:(\d\d\d\d-\d\d-\d\d)", post_info).groups()[0]
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            vacations_days = (end_date - start_date).days + 1
            push_data = {}
            for id_want_vacation in ids_want_vacation:
                push_data[id_want_vacation] = {}
                for i in range(vacations_days):
                    date = start_date + datetime.timedelta(i)
                    try:
                        push_data[id_want_vacation][datetime.datetime.strftime(date, "%Y-%m-%d")] = \
                        self.session.query(WorkArrangement.type).filter(WorkArrangement.date == date,
                                                                        WorkArrangement.worker_id == id_want_vacation).first()[0]
                    except:
                        print('数据库读取问题，可能是当前日期未排班')

        else:
            vacation_data=re.findall("\[(.*?)\]",post_info)
            SQL_str="REPLACE INTO vacation(worker_id,date,start_time,end_time,hours,vacation_type,audit_state,submit_id) VALUES "
            for item in vacation_data:
                SQL_str+='('+item+'),'
            conn=self.engine.connect()
            conn.execute(SQL_str[:-1])
            push_data={'code':200}
            print(vacation_data)
        print(push_data)
        self.finish(push_data)

