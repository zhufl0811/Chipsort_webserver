from methods.ormoperator import OrmOperator
import tornado.web
from ..basehandler import BaseHandler
from models import auth
from urllib.parse import urlparse

class EditPerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        url = urlparse(self.request.uri).query.split('=')[1]
        oo_rp = OrmOperator(auth.RolePermission)
        role_old = oo_rp.query_all('role_name',url=url)
        oo_r = OrmOperator(auth.Role)
        roles = oo_r.query_all('role_name')
        self.render('admin/editper.html',url=url,role_old=role_old,roles=roles)

    def post(self):
        url = urlparse(self.request.uri).query.split('=')[1]
        new_role = self.get_arguments('role_selected[]')
        oo_rp = OrmOperator(auth.RolePermission)
        oo_rp.delete(url=url)
        for role in new_role:
            oo_rp.add_row(url=url,role_name=role)
        self.write('''<head><script>setTimeout("javascript:location.href='/admin/delper'", 1500);</script></head>
                                        <h2 align='center'>修改成功，将跳转到之前页</h2>''')