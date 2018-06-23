import tornado.web
from handlers.basehandler import BaseHandler
from models.attendance import WorkArrangementTime
from methods.ormoperator import OrmOperator
from models.info import EmployeeInservice
import datetime

class WaTypeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        oo_w = OrmOperator(WorkArrangementTime)
        wa_types = oo_w.query_all()
        worker_id=str(self.get_secure_cookie('worker_id'),encoding = 'utf-8')
        worker_name = OrmOperator(EmployeeInservice).query_all('name',worker_id=worker_id)[0]
        data={}
        data['worker_id']=worker_id
        data['worker_name']=worker_name
        type_info=[]
        for type in wa_types:
            temp_dict={}
            temp_dict['typename']=type.typename
            temp_dict['start_time'] = str(type.start_time)[:-3]
            temp_dict['end_time'] = str(type.end_time)[:-3]
            temp_dict['inuse'] = type.inuse
            temp_dict['readonly']=True
            type_info.append(temp_dict)
        data['type_info']=type_info
        self.write(data)
        print(data)
    def post(self):
        if 'start_time' in str(self.request.body, encoding = 'utf-8'):
            data = str(self.request.body, encoding = 'utf-8')[1:-1].replace('\"', '').split(',')
            wa_type = {}
            for info in data:
                info = info.split(':')
                if len(info) == 2:
                    if info[0] == 'inuse':
                        if info[1] == 'false':
                            wa_type[info[0]] = 0
                        else:
                            wa_type[info[0]] = 1
                    else:
                        wa_type[info[0]] = info[1]
                else:
                    wa_type[info[0]] = info[1] + ':' + info[2] + ':' + '00'
            if 'readonly' in wa_type:
                del wa_type['readonly']
            oo_w = OrmOperator(WorkArrangementTime)
            if wa_type['typename'] in oo_w.query_all('typename'):
                oo_w.delete(typename = wa_type['typename'])
            oo_w.add_row(**wa_type)
            self.write({'code': 200})
        else:
            data = str(self.request.body, encoding = 'utf-8')[1:-1].replace('\"', '')
            oo_w=OrmOperator(WorkArrangementTime)
            oo_w.delete(typename=data[9:])
            self.write({'code': 200})