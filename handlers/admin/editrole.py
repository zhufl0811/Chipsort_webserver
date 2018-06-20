from methods.ormoperator import OrmOperator
import tornado.web
from ..basehandler import BaseHandler
from models import auth
from urllib.parse import urlparse,unquote

class EditRoleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        role_name = unquote((urlparse(self.request.uri).query).split('=')[1])
        oo_ur = OrmOperator(auth.UserRole)
        oo_rp = OrmOperator(auth.RolePermission)
        users_is_this_role = oo_ur.query_all('worker_id',role_name=role_name)
        url_this_role_own = oo_rp.query_all('url',role_name=role_name)
        all_user = OrmOperator(auth.User).query_all('worker_id')
        all_url = (OrmOperator(auth.Permission)).query_all('url')
        url_basic=[]
        url_admin=[]
        url_attendance=[]
        for url in all_url:
            if url.startswith('/admin'):
                url_admin.append(url)
            elif url.startswith('/attendance'):
                url_attendance.append(url)
            else:
                url_basic.append(url)
        all_url = {'基本':url_basic,'管理员':url_admin,'考勤系统':url_attendance}
        self.render('admin/editrole.html',role_name=role_name,all_user=all_user,all_url=all_url,
                    url_this_role_own=url_this_role_own,users_is_this_role=users_is_this_role)

    def post(self):
        role_name = unquote((urlparse(self.request.uri).query).split('=')[1])
        new_worker = self.get_arguments('worker_id_selected[]')
        new_url = self.get_arguments('url_selected[]')
        oo_ur = OrmOperator(auth.UserRole)
        oo_ur.delete(role_name=role_name)
        for worker in new_worker:
            oo_ur.add_row(role_name=role_name,worker_id=worker)
        oo_rp = OrmOperator(auth.RolePermission)
        oo_rp.delete(role_name=role_name)
        for url in new_url:
            oo_rp.add_row(role_name=role_name,url=url)
        self.write('''<script>
                                        alert('修改成功');
                                        window.location='/admin/delrole'
                                    </script>''')