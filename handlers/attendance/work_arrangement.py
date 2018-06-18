import tornado.web
from handlers.basehandler import BaseHandler
from models.info import EmployeeInservice
from models.attendance import DIYGroupDivide
from methods.ormoperator import OrmOperator
import json

class WorkArrangementHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        worker_id = str(self.get_secure_cookie('worker_id'),encoding = 'utf-8')
        oo_e=OrmOperator(EmployeeInservice)
        group_of_thisid = oo_e.query_all('dep_job',worker_id=worker_id)
        oo_diy = OrmOperator(DIYGroupDivide)
        push_data = {
            'worker_id': worker_id,
            'group_info':[]
        }
        if group_of_thisid[0][-2:]=='经理':
            dep = group_of_thisid[0][:2]
            members_in_this_dep = oo_e.query_like('dep_job',dep)
            groups_be_operated = list(set([member.dep_job for member in members_in_this_dep]))
            groups_be_operated.remove(group_of_thisid[0])
        else:
            groups_be_operated=group_of_thisid
        for group in groups_be_operated:
            group_member_info = []
            members_info = oo_e.query_all('worker_id', 'name', dep_job = group)
            for i in range(len(members_info['worker_id'])):
                group_member_info.append({'id': members_info['worker_id'][i], 'name': members_info['name'][i]})
            diy_info = []
            group_diy_info = oo_diy.query_all('group_son', 'ids_in_son', operator_id = worker_id, group_parent = group)
            for j in range(len(group_diy_info['group_son'])):
                diy_info.append(
                    {'son_group_name': group_diy_info['group_son'][j], 'ids_in_son': group_diy_info['ids_in_son'][j]})
            info_of_this_group = {
                'group_name': group,
                'group_members': group_member_info,
                'diy_info': diy_info
            }
            push_data['group_info'].append(info_of_this_group)
        self.write(push_data)

    def post(self):
        data=str(self.request.body,encoding = 'utf-8')[1:-1].replace('\"','').split(',')
        data_dict={}
        for item in data:
            item=item.split(':')
            data_dict[item[0]]=item[1]
        print(data_dict)
        self.write({'code':200})