import tornado.web
from ..basehandler import BaseHandler
from models.attendance import OverTime, WorkArrangement, WorkArrangementTime
from models.info import EmployeeInservice
from models.auth import UserRole
import re

class OverTimeAuditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        roles=[role[0] for role in self.session.query(UserRole.role_name).filter(UserRole.worker_id==self.worker_id).all()]
        groups_ids_dict = {}
        if 'admin' in roles or '人事' in roles:
            groups=list(set([group[0] for group in self.session.query(EmployeeInservice.dep_job).all()]))
        else:
            dep=self.session.query(EmployeeInservice.dep_job).filter(EmployeeInservice.worker_id==self.worker_id).first()[0][:2]
            groups = list(set([group[0] for group in self.session.query(EmployeeInservice.dep_job).filter(EmployeeInservice.dep_job.like(dep+'%'),EmployeeInservice.dep_job.notlike('%经理')).all()]))
        worker_ids_unaudited=[]
        for group in groups:
            ids=[id[0] for id in self.session.query(EmployeeInservice.worker_id).filter(EmployeeInservice.dep_job==group).all()]
            groups_ids_dict[group]=ids
            worker_ids_unaudited.extend(ids)
        dates_unaudited=[date[0] for date in self.session.query(OverTime.date).filter(OverTime.worker_id.in_(worker_ids_unaudited),OverTime.audit_state==False).all()]
        dates_unaudited=[str(date) for date in list(set(dates_unaudited))]
        push_data={'worker_id':self.worker_id,'worker_name':self.id_name[self.worker_id],'id_name':self.id_name,'id_group':self.id_group,'overtime_unaudited_info':{}}
        for date in dates_unaudited:
            push_data['overtime_unaudited_info'][date]={}
            for group in groups_ids_dict:
                push_data['overtime_unaudited_info'][date][group] = []
                ot_objs=self.session.query(OverTime).filter(OverTime.date==date,OverTime.audit_state==0,OverTime.worker_id.in_(groups_ids_dict[group])).order_by(OverTime.start_time).all()
                for ot_obj in ot_objs:
                    temp = []
                    temp.append(ot_obj.worker_id)
                    work_type_thisday=self.session.query(WorkArrangement.type).filter(WorkArrangement.worker_id==ot_obj.worker_id,WorkArrangement.date==date).first()[0]
                    temp.append(work_type_thisday)
                    work_type_starttime=self.session.query(WorkArrangementTime.start_time).filter(WorkArrangementTime.typename==work_type_thisday).first()[0]
                    work_type_endtime=self.session.query(WorkArrangementTime.end_time).filter(WorkArrangementTime.typename==work_type_thisday).first()[0]
                    temp.append(str(work_type_starttime)[:-3])
                    temp.append(str(work_type_endtime)[:-3])
                    temp.append(str(ot_obj.start_time)[:-3])
                    temp.append(str(ot_obj.end_time)[:-3])
                    temp.append(str(ot_obj.worker_id))
                    temp.append(ot_obj.hours)
                    temp.append(ot_obj.ratio)
                    temp.append(ot_obj.submit_id)
                    push_data['overtime_unaudited_info'][date][group].append(temp)
        print(push_data['overtime_unaudited_info'])
        self.finish(push_data)
    @tornado.web.authenticated
    def post(self):
        post_info=str(self.request.body,encoding='utf-8')[1:-1]
        print(post_info)
        operate_date=re.search('date:(\d{4}-\d\d-\d\d)',post_info.replace('\"','')).groups()[0]
        ids='('+re.search('\"ids\":\[(.*)\]',post_info).groups()[0]+')'
        pass_or_not=re.search('pass_or_not:(\d)',post_info.replace('\"','')).groups()[0]
        conn = self.engine.connect()
        if pass_or_not=='1':
            SQL_str="UPDATE overtime SET audit_state=1, audit_id='{audit_id}' WHERE date='{date}' and worker_id in {ids}".format(audit_id=self.worker_id,
                                                                                                                             date=operate_date,
                                                                                                                             ids=ids)
        else:
            SQL_str="DELETE FROM overtime WHERE date='{date}' and worker_id in {ids}".format(date=operate_date,ids=ids)
        print(SQL_str)
        conn.execute(SQL_str)
        self.finish({'code':200})