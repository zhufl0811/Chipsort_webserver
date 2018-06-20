import tornado.web
from ..basehandler import BaseHandler
from models import auth
from methods.ormoperator import OrmOperator

class AddPerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        oo_roles = OrmOperator(auth.Role)
        role_name = oo_roles.query_all('role_name')
        self.render('admin/addper.html',roles = role_name)

    def post(self):
        url = self.get_argument('url')
        desc = self.get_argument('desc')
        role_selected=self.get_arguments('role_selected[]')
        try:
            oo_per = OrmOperator(auth.Permission)
            oo_per.add_row(url = url, description = desc)
            for role in role_selected:
                oo_role_per = OrmOperator(auth.RolePermission)
                oo_role_per.add_row(url = url, role_name = role)
            # self.write('''<head><script>setTimeout("javascript:location.href='/admin/addper'", 1500);</script></head>
            #         <h2>添加成功，将跳转到之前页</h2>''')
            self.write('''<script>
                alert('添加成功');
                window.location='/admin/addper'
            </script>''')
        except Exception as e:
            self.write('''<h2>错误：%s</h2><a href='/admin/addper'>返回</a>''' %e.args)


