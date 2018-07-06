import tornado.web
from ..basehandler import BaseHandler
from models.attendance import OverTime, WorkArrangement, WorkArrangementTime
from models.info import EmployeeInservice
import re,time,datetime
from methods.str_date_plus_one import str_date_plus_one

class OverTimeSubmitHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        worker_id=str(self.get_secure_cookie('worker_id'),encoding='utf-8')
        worker_name=self.session.query(EmployeeInservice.name).filter(EmployeeInservice.worker_id==worker_id).first()[0]
        group=self.session.query(EmployeeInservice.dep_job).filter(EmployeeInservice.worker_id==worker_id).first()[0]
        dep=group[:2]
        if group[3:]=='经理':
            group = self.session.query(EmployeeInservice.dep_job).filter(EmployeeInservice.dep_job.like(group[:2]+'%')).filter(EmployeeInservice.dep_job.notlike('%'+group[3:])).all()
            group=list(set(group))
            for i in range(len(group)):
                group[i]=group[i][0]
            group.append(dep+'|全体')
        else:
            group=[group]
        push_data={
            'worker_id':worker_id,
            'worker_name':worker_name,
            'group':group,
            'id_name':{}
        }
        for item in self.session.query(EmployeeInservice.worker_id,EmployeeInservice.name).all():
            push_data['id_name'][item[0].lower()] = item[1]
            push_data['id_name'][item[0].upper()] = item[1]
        self.finish(push_data)

    def post(self):
        post_data=str(self.request.body,encoding='utf-8')[1:-1].replace('"','')
        submit_id=str(self.get_secure_cookie('worker_id'),encoding='utf-8')
        if 'start_time_hour' in post_data: #此为加班提报的处理方式
            print(post_data)
            start_time = re.search('start_time_hour:(\d\d)',post_data).groups()[0]+':'+re.search('start_time_min:(\d\d)',post_data).groups()[0]
            end_time = re.search('end_time_hour:(\d\d)',post_data).groups()[0]+':'+re.search('end_time_min:(\d\d)',post_data).groups()[0]
            ids = re.search('ids:\[(.*?)\]',post_data).groups()[0].split(',')
            kind = re.search('kind:(.*?),',post_data).groups()[0]
            date = re.search('date:(\d{4}-\d\d-\d\d)',post_data).groups()[0]
            group_type=re.search('group_type:(.*)',post_data).groups()[0]
            type_info = self.session.query(WorkArrangementTime).filter(WorkArrangementTime.typename==group_type[6:]).first()
            if kind=='kind1':
                #如果加班类型为1，那么如果此时上夜班（排班时间跨天），则报的加班时间日期增加一天，如果是白班，则加班时间的日期为当天
                #如果加班类型为2，那么如果此时所报的加班开始时间大于结束时间，则默认此时是加夜班（加班时间跨天），结束时间的日期会增加1天，如果不是，则加班时间的日期为当天
                hours = int(end_time[:2]) - int(start_time[:2]) + (int(end_time[3:]) - int(start_time[3:])) / 60
                if type_info.start_time > type_info.end_time:
                    start_time = str_date_plus_one(date) + ' ' + start_time
                    end_time = str_date_plus_one(date) + ' ' + end_time
                else:
                    start_time = date + ' ' + start_time
                    end_time = date + ' ' + end_time
                ratio=1.5
            else:
                if int(end_time[:2])<int(start_time[:2]):
                    hours = int(end_time[:2]) - int(start_time[:2]) +24+ (int(end_time[3:]) - int(start_time[3:])) / 60
                    start_time = date + ' ' + start_time
                    end_time = str_date_plus_one(date) + ' ' + end_time
                else:
                    hours = int(end_time[:2]) - int(start_time[:2]) + (int(end_time[3:]) - int(start_time[3:])) / 60
                    start_time = date + ' ' + start_time
                    end_time = date + ' ' + end_time
                ratio=2.0
            SQL_str = 'REPLACE INTO overtime (worker_id,date,start_time,end_time,hours,ratio,audit_state,submit_id) VALUES '
            for id in ids:
                SQL_str+=('(\''+id+'\',\''+date+'\',\''+start_time+'\',\''+end_time+'\',\''+
                          str(hours)+'\',\''+str(ratio)+'\',\''+'0'+'\',\''+submit_id+'\'),')
            SQL_str=SQL_str[:-1]
            conn = self.engine.connect()
            conn.execute(SQL_str)
            self.finish({'code':'200'})
        else: #此为最初选定日期后的返回数据
            query_info = post_data.split(',')
            wa_types = self.session.query(WorkArrangementTime.typename).filter(WorkArrangementTime.inuse == True).all()
            wa_types = [typee[0] for typee in wa_types]
            group = query_info[0].split(':')[1]
            date = query_info[1].split(':')[1]
            if group[3:] == '全体':
                groups = self.session.query(EmployeeInservice.dep_job).filter(
                    EmployeeInservice.dep_job.like(group[:2] + '%')).filter(
                    EmployeeInservice.dep_job.notlike('%经理')).all()
                groups = list(set(groups))
                for i in range(len(groups)):
                    groups[i] = groups[i][0]
            else:
                groups = [group]
            push_data = {'group_type_info': {},'overtime_info':{'unaudited':[],'audited':[]}}
            for gro in groups:
                push_data['group_type_info'][gro] = {}
                ids_this_gro = [id[0] for id in self.session.query(EmployeeInservice.worker_id).filter(
                    EmployeeInservice.dep_job == gro).all()]
                for typee in wa_types:
                    ids_this_gro_type = [id[0] for id in
                                         self.session.query(
                                             WorkArrangement.worker_id).filter(WorkArrangement.type == typee,
                                                                               WorkArrangement.worker_id.in_(
                                                                                   ids_this_gro),
                                                                               WorkArrangement.date == date).all()]
                    push_data['group_type_info'][gro][typee] = ids_this_gro_type
            unaudited_objs=self.session.query(OverTime).filter(OverTime.date==date,OverTime.submit_id==submit_id,OverTime.audit_state==False).order_by(OverTime.start_time).all()
            for unaudited_obj in unaudited_objs:
                uo_id=unaudited_obj.worker_id
                temp=[]
                #push_data['overtime_info']['unaudited']的数据：[工号，排班类型，排班开始时间，排班结束时间，加班开始，加班结束，加班时长，比例，提报人工号，审核人工号，状态]
                temp.append(uo_id)
                uo_type=self.session.query(WorkArrangement.type).filter(WorkArrangement.worker_id==uo_id,WorkArrangement.date==date).first()[0]
                temp.append(uo_type)
                uo_type_time=self.session.query(WorkArrangementTime.start_time,WorkArrangementTime.end_time).filter(WorkArrangementTime.typename==uo_type).all()[0]
                temp.append(str(uo_type_time[0])[:-3])
                temp.append(str(uo_type_time[1])[:-3])
                temp.append(str(unaudited_obj.start_time)[:-3])
                temp.append(str(unaudited_obj.end_time)[:-3])
                temp.append(unaudited_obj.hours)
                temp.append(unaudited_obj.ratio)
                temp.append(unaudited_obj.submit_id)
                temp.append(unaudited_obj.audit_id)
                temp.append('未审核')
                push_data['overtime_info']['unaudited'].append(temp)
            audited_objs = self.session.query(OverTime).filter(OverTime.date == date, OverTime.submit_id == submit_id,
                                                                 OverTime.audit_state == True).order_by(OverTime.start_time).all()
            for audited_obj in audited_objs:
                a_id = audited_obj.worker_id
                temp = []
                # push_data['overtime_info']['audited']的数据：[工号，排班类型，排班开始时间，排班结束时间，加班开始，加班结束，加班时长，比例，提报人工号，审核人工号，状态]
                temp.append(a_id)
                a_type = self.session.query(WorkArrangement.type).filter(WorkArrangement.worker_id == a_id,
                                                                          WorkArrangement.date == date).first()[0]
                temp.append(a_type)
                a_type_time = self.session.query(WorkArrangementTime.start_time, WorkArrangementTime.end_time).filter(
                    WorkArrangementTime.typename == a_type).all()[0]
                temp.append(str(a_type_time[0])[:-3])
                temp.append(str(a_type_time[1])[:-3])
                temp.append(str(audited_obj.start_time)[:-3])
                temp.append(str(audited_obj.end_time)[:-3])
                temp.append(audited_obj.hours)
                temp.append(audited_obj.ratio)
                temp.append(audited_obj.submit_id)
                temp.append(audited_obj.audit_id)
                temp.append('已审核')
                push_data['overtime_info']['unaudited'].append(temp)
            print(push_data)
            self.finish(push_data)