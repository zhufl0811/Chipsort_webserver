from methods.ormoperator import OrmOperator
import tornado.web
from ..basehandler import BaseHandler
from models import auth
from urllib.parse import urlparse

class EditUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        if urlparse(self.request.uri).query:
            worker_id = (urlparse(self.request.uri).query).split('=')[1]
            oo_ur=OrmOperator(auth.UserRole)
            roles_own_by_thisid = oo_ur.query_all('role_name',worker_id=worker_id)
            oo_r = OrmOperator(auth.Role)
            role_list = oo_r.query_all('role_name')
            user_info = [worker_id,roles_own_by_thisid,role_list]
            self.render('admin/edituser.html',user_info=user_info)
        else:
            self.render('admin/edituser.html',user_info=['','',''])
    def post(self,*args):
        worker_id = (urlparse(self.request.uri).query).split('=')[1]
        oo_ur = OrmOperator(auth.UserRole)
        oo_ur.delete(worker_id=worker_id)
        new_role = self.get_arguments('role_selected[]')
        for role in new_role:
            oo_ur.add_row(worker_id=worker_id,role_name=role)
        self.write('''<script>
                                        alert('修改成功');
                                        window.location='/admin/deluser'
                                    </script>''')