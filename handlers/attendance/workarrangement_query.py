import tornado.web
from handlers.basehandler import BaseHandler
from models.info import EmployeeInservice
from models.attendance import WorkArrangement,WorkArrangementTime
from methods.ormoperator import OrmOperator
import datetime
import re,json

class WAQueryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        worker_id=self.get_secure_cookie('worker_id')
        oo_e=OrmOperator(EmployeeInservice)
        worker_name=oo_e.query_all('name',worker_id=worker_id)[0]
        id_name = oo_e.query_all('worker_id', 'name','dep_job')
        id_name_dict = {}
        id_group_dict={}
        for i in range(len(id_name['name'])):
            id_name_dict[id_name['worker_id'][i].lower()]=id_name['name'][i]
            id_name_dict[id_name['worker_id'][i].upper()] = id_name['name'][i]
            id_group_dict[id_name['worker_id'][i].lower()] = id_name['dep_job'][i]
            id_group_dict[id_name['worker_id'][i].upper()] = id_name['dep_job'][i]
        oo_t = OrmOperator(WorkArrangementTime)
        type_info = oo_t.query_all('typename','start_time','end_time')
        type_info_push={}
        for i in range(len(type_info['typename'])):
            type_info_push[type_info['typename'][i]]={'start_time':str(type_info['start_time'][i]),'end_time':str(type_info['end_time'][i])}
        type_info_push['worker_name']=worker_name
        type_info_push['id_name']=id_name_dict
        type_info_push['id_group'] = id_group_dict
        print(type_info_push)
        self.finish(type_info_push)

    @tornado.web.authenticated
    def post(self):
        query_contidion=str(self.request.body,encoding='utf-8')[1:-1].replace('\"','').split(',')
        query_contidion_dict={}
        for condition in query_contidion:
            query_contidion_dict[condition.split(':')[0]]=condition.split(':')[1]
        start_date=datetime.datetime.strptime(query_contidion_dict['start_date'],'%Y-%m-%d')
        end_date=datetime.datetime.strptime(query_contidion_dict['end_date'],'%Y-%m-%d')

        oo_w=OrmOperator(WorkArrangement)
        push_data={'worker_id':[],'date':[],'type':[],'operator_id':[]}
        if query_contidion_dict['worker_id']:
            if query_contidion_dict['type']:
                query_datas = self.session.query(WorkArrangement).filter(WorkArrangement.worker_id==query_contidion_dict['worker_id'],
                                                                        WorkArrangement.type==query_contidion_dict['type'],
                                                                         WorkArrangement.date>=start_date,
                                                                         WorkArrangement.date<=end_date).all()
            else:
                query_datas = self.session.query(WorkArrangement).filter(WorkArrangement.worker_id == query_contidion_dict['worker_id'],
                                                                         WorkArrangement.date>=start_date,
                                                                         WorkArrangement.date<=end_date).all()
        elif query_contidion_dict['group']:
            if '全体' in query_contidion_dict['group']:
                ids_in_group=[person.worker_id for person in OrmOperator(EmployeeInservice).query_like('dep_job',query_contidion_dict['group'][:3])]
                print(ids_in_group,len(ids_in_group))
            else:
                ids_in_group=OrmOperator(EmployeeInservice).query_all('worker_id',dep_job=query_contidion_dict['group'])
            if query_contidion_dict['type']:
                query_datas = self.session.query(WorkArrangement).filter(
                    WorkArrangement.worker_id.in_(ids_in_group),
                    WorkArrangement.type == query_contidion_dict['type'],
                    WorkArrangement.date >= start_date,
                    WorkArrangement.date <= end_date).all()
                # for id in ids_in_group:
                #     for i in range((end_date - start_date).days + 1):
                #         date = datetime.datetime.strftime(start_date + datetime.timedelta(i), '%Y-%m-%d')
                #         temp = oo_w.query_all('worker_id', 'date', 'type', 'operator_id',
                #                               date=date, worker_id=id,type=query_contidion_dict['type'])
                #         push_data['worker_id'].extend(temp['worker_id'])
                #         push_data['type'].extend(temp['type'])
                #         push_data['operator_id'].extend(temp['operator_id'])
                #         for dd in temp['date']:
                #             push_data['date'].append(datetime.datetime.strftime(dd, '%Y-%m-%d'))
            else:
                query_datas = self.session.query(WorkArrangement).filter(
                    WorkArrangement.worker_id.in_(ids_in_group),
                    WorkArrangement.date >= start_date,
                    WorkArrangement.date <= end_date).all()
                # for id in ids_in_group:
                #     for i in range((end_date - start_date).days + 1):
                #         date = datetime.datetime.strftime(start_date + datetime.timedelta(i), '%Y-%m-%d')
                #         temp = oo_w.query_all('worker_id', 'date', 'type', 'operator_id',
                #                               date=date, worker_id=id)
                #         push_data['worker_id'].extend(temp['worker_id'])
                #         push_data['type'].extend(temp['type'])
                #         push_data['operator_id'].extend(temp['operator_id'])
                #         for dd in temp['date']:
                #             push_data['date'].append(datetime.datetime.strftime(dd, '%Y-%m-%d'))
        else:
            query_datas = self.session.query(WorkArrangement).filter(
                WorkArrangement.type == query_contidion_dict['type'],
                WorkArrangement.date >= start_date,
                WorkArrangement.date <= end_date).all()
        for query_data in query_datas:
            push_data['worker_id'].append(query_data.worker_id)
            push_data['type'].append(query_data.type)
            push_data['operator_id'].append(query_data.operator_id)
            push_data['date'].append(datetime.datetime.strftime(query_data.date, '%Y-%m-%d'))
        self.finish(push_data)