from methods.get_all_user_info import get_all_role_info
from methods.ormoperator import OrmOperator
import tornado.web
from ..basehandler import BaseHandler
from models.auth import *


class DelRoleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        role_info = get_all_role_info()
        for role in role_info:
            role[2] = '【'+'】，【'.join(role[2].split(','))+'】'
        self.render('admin/delrole.html',role_info=role_info)
    def post(self):
        role_name = self.get_argument('delete')
        if role_name == 'admin':
            self.write('''<head><script>setTimeout("javascript:location.href='/admin/delrole'", 1500);</script></head>
                                        <h2>无法删除管理员，将跳转到之前页</h2>''')
        else:
            oo_r = OrmOperator(Role)
            oo_r.delete(role_name = role_name)
            oo_ur = OrmOperator(UserRole)
            oo_ur.delete(role_name=role_name)
            oo_rp = OrmOperator(RolePermission)
            oo_rp.delete(role_name=role_name)
            self.write('''<script>
                                    alert('删除成功');
                                    window.location='/admin/delrole'
                                </script>''')