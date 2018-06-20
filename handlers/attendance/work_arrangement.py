import tornado.web
from handlers.basehandler import BaseHandler
from models.info import EmployeeInservice
from models.attendance import DIYGroupDivide
from models.attendance import WorkArrangement
from methods.ormoperator import OrmOperator
import datetime
import re

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
        if group_of_thisid[0][-2:]=='经理':#如果是经理级别，那么就获得该部门的所有分组信息。
            dep = group_of_thisid[0][:2]
            members_in_this_dep = oo_e.query_like('dep_job',dep)
            groups_be_operated = list(set([member.dep_job for member in members_in_this_dep]))
            groups_be_operated.remove(group_of_thisid[0])#groups_be_operated为该部门groups的列表（除经理外）
        else:#如果不是经理，则只获得其所在组的信息。因为若能访问此url，则必为组长级别，所以普工无法进入此url
            groups_be_operated=group_of_thisid #单元素列表

        for group in groups_be_operated:
            group_member_info = []
            members_info = oo_e.query_all('worker_id', 'name', dep_job = group)
            for i in range(len(members_info['worker_id'])):
                group_member_info.append({'id': members_info['worker_id'][i], 'name': members_info['name'][i]})
            diy_group_info = []
            group_diy_info = oo_diy.query_all('group_son', 'ids_in_son', operator_id = worker_id, group_parent = group)
            ids_been_diyed=''
            for j in range(len(group_diy_info['group_son'])):
                diy_group_info.append(
                    {'son_group_name': group_diy_info['group_son'][j], 'ids_in_son': group_diy_info['ids_in_son'][j]})
                ids_been_diyed+=(','+group_diy_info['ids_in_son'][j])
            ids_not_diyed = list(set(members_info['worker_id'])-set(ids_been_diyed.split(',')))
            diy_info={'ids_not_diyed':ids_not_diyed,'diy_group_info':diy_group_info}
            info_of_this_group = {
                'group_name': group,
                'group_members': group_member_info,
                'diy_info': diy_info
            }
            push_data['group_info'].append(info_of_this_group)
        self.write(push_data)

    @tornado.web.authenticated
    def post(self):
        if re.match(b'.*?son_group_name',self.request.body):
            data = str(self.request.body, encoding = 'utf-8')[1:-1].replace('\"', '')
            son_group_name = re.search("son_group_name:(.*?),",data).groups()[0]
            ids_divided_into = re.search("ids_divided_into:\[(.*?)\]", data).groups()[0]
            oo_e=OrmOperator(EmployeeInservice)
            group_parent=oo_e.query_all('dep_job',worker_id=ids_divided_into[:4])[0]
            oo_d = OrmOperator(DIYGroupDivide)
            operator_id = self.get_secure_cookie('worker_id')
            oo_d.add_row(operator_id=operator_id,
                         group_parent=group_parent,
                         group_son=son_group_name,
                         ids_in_son=ids_divided_into)
            self.write({'code': 200})
        elif re.match(b'.*?group_parent',self.request.body):
            data=str(self.request.body, encoding = 'utf-8')[1:-1].replace('\"','').split(',')
            group_parent=data[0].split(':')[1]
            group_son_del = data[1].split(':')[1][4:]
            oo_d=OrmOperator(DIYGroupDivide)
            oo_d.delete(operator_id=self.get_secure_cookie('worker_id'),
                        group_parent=group_parent,
                        group_son=group_son_del)
            self.write({'code': 200})
        else:
            # 以下5行解析JSON数据（有点麻烦），得到一个字典
            data = str(self.request.body, encoding = 'utf-8')[1:-1].replace('\"', '').split(',')
            data_dict = {}
            for item in data:
                item = item.split(':')
                data_dict[item[0]] = item[1]
            # 以下2行取得开始和结束日期，并将他们从字典中删除，只留下工号和排班种类信息
            start_date = datetime.datetime.strptime(data_dict.pop('start_date'), '%Y-%m-%d')
            end_date = datetime.datetime.strptime(data_dict.pop('end_date'), '%Y-%m-%d')
            # 开始操作数据库
            oo_wa = OrmOperator(WorkArrangement)
            id_list = []
            type_list = []
            # 得到id和种类的列表，方便传入OrmOperator.add_some_row中
            for key in data_dict:
                id_list.append(key)
                type_list.append(data_dict[key])
            operate_days = (end_date - start_date).days + 1
            operator_id = [str(self.get_secure_cookie('worker_id'), encoding = 'utf-8')] * len(id_list)
            for i in range(operate_days):
                date = start_date + datetime.timedelta(i)
                # #先判断是否存在，存在则删除
                # for key in data_dict:
                #     if oo_wa.query_all(date=date,worker_id=key):
                #         oo_wa.delete(date=date,worker_id=key)
                date_list = [date] * len(id_list)
                oo_wa.delete_some_row(date = date_list, worker_id = id_list)
                # 一次性添加一个日期中所有员工的排班
                oo_wa.add_some_row(date = date_list, worker_id = id_list,
                                   type = type_list, operator_id = operator_id)
            self.write({'code': 200})