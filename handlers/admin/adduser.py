from methods.ormoperator import OrmOperator
import tornado.web
from ..basehandler import BaseHandler
from models import auth
from methods.psd_to_md5 import psd_to_md5

class AddUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        oo_roles = OrmOperator(auth.Role)
        role_name = oo_roles.query_all('role_name')
        self.render('admin/adduser.html',roles = role_name)
    def post(self):
        worker_id = self.get_argument('worker_id')
        init_psd = self.get_argument('init_psd')
        role_selected = self.get_arguments('role_selected[]')
        try:
            oo_per = OrmOperator(auth.User)
            oo_per.add_row(worker_id=worker_id, psd = psd_to_md5(init_psd))
            for role in role_selected:
                oo_role_per = OrmOperator(auth.UserRole)
                oo_role_per.add_row(worker_id=worker_id, role_name = role)
            self.write('''<head><script>setTimeout("javascript:location.href='/admin/adduser'", 1500);</script></head>
                    <h2>添加成功，将跳转到之前页</h2>''')
        except Exception as e:
            self.write('''<h2>错误：%s</h2><a href='/admin/addper'>返回</a>''' %e.args)
