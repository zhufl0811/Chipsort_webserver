import tornado.web
from handlers.basehandler import BaseHandler
from models.info import EmployeeInservice
from models.attendance import DIYGroupDivide
from models.attendance import WorkArrangement,WorkArrangementTime
from methods.ormoperator import OrmOperator
import datetime
import re

class WorkArrangementHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        worker_id = str(self.get_secure_cookie('worker_id'), encoding = 'utf-8')
        oo_wt=OrmOperator(WorkArrangementTime)
        workarrange_types = oo_wt.query_all('typename',inuse=True)
        oo_e = OrmOperator(EmployeeInservice)
        group_of_thisid = oo_e.query_all('dep_job', worker_id = worker_id)[0]
        worker_name = oo_e.query_all('name', worker_id = worker_id)[0]
        oo_diy = OrmOperator(DIYGroupDivide)
        push_data = {
            'worker_id': worker_id,
            'worker_name': worker_name,
            'workarrangement_types':workarrange_types,
            'group_info': []
        }
        if group_of_thisid[-2:]=='经理':#如果是经理级别，那么就获得该部门的所有分组信息。
            dep = group_of_thisid[:2]
            members_in_this_dep = oo_e.query_like('dep_job',dep)
            groups_be_operated = list(set([member.dep_job for member in members_in_this_dep]))
            groups_be_operated.remove(group_of_thisid)#groups_be_operated为该部门groups的列表（除经理外）
        else:#如果不是经理，则只获得其所在组的信息。因为若能访问此url，则必为组长级别，所以普工无法进入此url
            groups_be_operated=[group_of_thisid] #单元素列表

        for group in groups_be_operated:
            group_member_info = {}
            members_info = oo_e.query_all('worker_id', 'name', dep_job = group)
            for i in range(len(members_info['worker_id'])):
                group_member_info[members_info['worker_id'][i]]=members_info['name'][i]
            diy_info = {}
            group_diy_info = oo_diy.query_all('group_son', 'ids_in_son', operator_id = worker_id, group_parent = group)
            ids_been_diyed=''
            for j in range(len(group_diy_info['group_son'])):
                ids_been_diyed += (',' + group_diy_info['ids_in_son'][j])
                diy_info[group_diy_info['group_son'][j]]=group_diy_info['ids_in_son'][j].split(',')
            ids_not_diyed = list(set(members_info['worker_id'])-set(ids_been_diyed.split(',')))
            diy_info['ids_not_diyed']=ids_not_diyed
            info_of_this_group = {
                'group_name': group,
                'group_members': group_member_info,
                'diy_info': diy_info
            }
            push_data['group_info'].append(info_of_this_group)
        self.write(push_data)

    @tornado.web.authenticated
    def post(self):
        data=str(self.request.body,encoding='utf-8')[1:-1].replace('\"','')
        start_date = re.search("start_date:(.*?),",data).groups()[0]
        start_date = datetime.date(int(start_date.split('-')[0]),int(start_date.split('-')[1]),
                                   int(start_date.split('-')[2]))
        end_date = re.search("end_date:(.*?),",data).groups()[0]
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]),
                                   int(end_date.split('-')[2]))
        wa_info_list=re.search("{(.*)}",data).groups()[0].split(',')
        wa_idtype_dict={}
        wa_id_list=[]
        wa_type_list=[]
        for info in wa_info_list:
            temp=info.split(':')
            wa_id_list.append(temp[0])
            wa_type_list.append(temp[1])
            wa_idtype_dict[temp[0]]=temp[1]
        wa_info_insert={'date':[],'worker_id':[],'type':[],'operator_id':[]}
        sum_days=(end_date-start_date).days+1
        for i in range(sum_days):
            wa_info_insert['date'].extend([start_date+datetime.timedelta(i)]*len(wa_id_list))
            wa_info_insert['worker_id'].extend(wa_id_list)
            wa_info_insert['type'].extend(wa_type_list)
        wa_info_insert['operator_id']=[self.get_secure_cookie('worker_id')]*len(wa_info_insert['date'])
        oo_w=OrmOperator(WorkArrangement)
        oo_w.delete_some_row(date=wa_info_insert['date'],worker_id=wa_info_insert['worker_id'])
        oo_w.add_some_row(date=wa_info_insert['date'],
                          worker_id=wa_info_insert['worker_id'],
                          type=wa_info_insert['type'],
                          operator_id=wa_info_insert['operator_id'])

        diy_info_insert={'operator_id':[],
                         'group_son':list(set(wa_type_list)),
                         'group_parent':[],#[OrmOperator(EmployeeInservice).query_all('dep_job',worker_id=wa_id_lis}
                         'ids_in_son':[]}
        for name in diy_info_insert['group_son']:
            ids_in_this_name=''
            for key in wa_idtype_dict:
                if wa_idtype_dict[key]==name:
                    ids_in_this_name+=(key+',')
            ids_in_this_name=ids_in_this_name[:-1]
            diy_info_insert['ids_in_son'].append(ids_in_this_name)
        diy_info_insert['operator_id']=[self.get_secure_cookie('worker_id')]*len(diy_info_insert['group_son'])
        diy_info_insert['group_parent']=[OrmOperator(EmployeeInservice).query_all('dep_job',worker_id=wa_id_list[0])]*len(diy_info_insert['group_son'])
        oo_d=OrmOperator(DIYGroupDivide)
        for i in range(len(diy_info_insert['operator_id'])):
            oo_d.delete(operator_id=diy_info_insert['operator_id'][i],group_parent=diy_info_insert['group_parent'][i])
        oo_d.add_some_row(operator_id=diy_info_insert['operator_id'],group_parent=diy_info_insert['group_parent'],
                          group_son=diy_info_insert['group_son'],ids_in_son=diy_info_insert['ids_in_son'])
        self.write({'code':200})