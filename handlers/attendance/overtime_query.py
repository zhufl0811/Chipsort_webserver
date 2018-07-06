import tornado.web
from ..basehandler import BaseHandler
from models.info import EmployeeInservice
from models.attendance import OverTime,WorkArrangementTime,WorkArrangement

class OverTimeQueryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        push_data={
            'worker_id':self.worker_id,
            'id_name':{}
        }
        employee_id_name=self.session.query(EmployeeInservice.worker_id,EmployeeInservice.name).all()
        for employee in employee_id_name:
            push_data['id_name'][employee[0].lower()]=employee[1]
            push_data['id_name'][employee[0].upper()]=employee[1]
        self.finish(push_data)
    def post(self):
        push_data=[]
        id_name_group={}
        employee_id_name_group = self.session.query(EmployeeInservice.worker_id, EmployeeInservice.name, EmployeeInservice.dep_job).all()
        for employee in employee_id_name_group:
            id_name_group[employee[0].lower()]={'name':employee[1],'group':employee[2]}
            id_name_group[employee[0].upper()]={'name':employee[1],'group':employee[2]}
        type_time=self.session.query(WorkArrangementTime.typename,WorkArrangementTime.start_time,WorkArrangementTime.end_time).all()
        worktype_time={}
        for item in type_time:
            worktype_time[item[0]]={'start_time':str(item[1])[:-3],'end_time':str(item[2])[:-3]}
        print(id_name_group,worktype_time)
        query_condition=str(self.request.body,encoding='utf-8')[1:-1].replace('\"','').split(',')
        start_date=query_condition[0].split(':')[1]
        end_date = query_condition[1].split(':')[1]
        overtime_info_objs=self.session.query(OverTime).filter(OverTime.date.between(start_date,end_date)).order_by(OverTime.date).all()
        info_for_filter={'groups':[],'names':[],'ratios':[],'states':[],'submit_ids':[],'audit_ids':[]}
        for obj in overtime_info_objs:
            work_type=self.session.query(WorkArrangement.type).filter(WorkArrangement.worker_id==obj.worker_id,WorkArrangement.date==obj.date).first()[0]
            temp=[]
            temp.append(str(obj.date)[2:])
            temp.append(obj.worker_id)
            temp.append(id_name_group[obj.worker_id]['name'])
            info_for_filter['names'].append(id_name_group[obj.worker_id]['name'])
            temp.append(id_name_group[obj.worker_id]['group'])
            info_for_filter['groups'].append(id_name_group[obj.worker_id]['group'])
            temp.append(work_type)
            temp.append(worktype_time[work_type]['start_time'])
            temp.append(worktype_time[work_type]['end_time'])
            temp.append(str(obj.start_time)[2:-3])
            temp.append(str(obj.end_time)[2:-3])
            temp.append(obj.hours)
            temp.append(obj.ratio)
            info_for_filter['ratios'].append(obj.ratio)
            info_for_filter['submit_ids'].append(id_name_group[obj.submit_id]['name'])
            temp.append(id_name_group[obj.submit_id]['name'])
            temp.append('已审核' if obj.audit_state else '未审核')
            info_for_filter['states'].append('已审核' if obj.audit_state else '未审核')
            if obj.audit_id:
                temp.append(id_name_group[obj.audit_id]['name'])
                info_for_filter['audit_ids'].append(id_name_group[obj.audit_id]['name'])
            else:
                temp.append('')
            push_data.append(temp)
        for key in info_for_filter:
            info_for_filter[key]=list(set(info_for_filter[key]))
            info_for_filter[key].insert(0,'全部')
        print(push_data)
        print(info_for_filter)
        self.finish({'return_info':push_data,'info_for_filter':info_for_filter})