import tornado.web
from ..basehandler import BaseHandler
import datetime
from models.attendance import Workday
from methods.ormoperator import OrmOperator

class WorkDayHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('attendance/workday.html',worker_id = self.get_secure_cookie('worker_id'))
    def post(self):
        start_date = datetime.datetime.strptime(self.get_argument('start_date'),"%Y-%m-%d")
        end_date = datetime.datetime.strptime(self.get_argument('end_date'),"%Y-%m-%d")
        sumdays = (end_date-start_date).days+1
        oo_wd = OrmOperator(Workday)
        workday_info = {}
        date_should_delete=[]
        for i in range(sumdays):
            date_str_with0 = (start_date+datetime.timedelta(days = i)).strftime('%Y-%m-%d')
            date_should_delete.append(date_str_with0)
            date_str = date_str_with0.split('-')
            if date_str[1][0] == '0':
                date_str[1] = date_str[1][1]
            if date_str[2][0] == '0':
                date_str[2] = date_str[2][1]
            date_str = '-'.join(date_str)
            workday_info[date_str_with0] = self.get_argument(date_str)
        oo_wd.delete_some_row(date_record=date_should_delete)
        oo_wd.add_some_row(date_record=list(workday_info.keys()),
                               mark=[workday_info[key] for key in list(workday_info.keys())])

        self.write('''<script>
                        alert('操作成功');
                        window.location='/attendance'
                    </script>''')