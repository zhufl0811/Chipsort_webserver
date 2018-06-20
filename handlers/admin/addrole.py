from methods.ormoperator import OrmOperator
import tornado.web
from ..basehandler import BaseHandler
from models import auth

class AddRoleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        oo_u = OrmOperator(auth.User)
        worker_ids = oo_u.query_all('worker_id')
        oo_p = OrmOperator(auth.Permission)
        urls = oo_p.query_all('url')
        url_basic = []
        url_admin = []
        url_attendance = []
        for url in urls:
            if url.startswith('/admin'):
                url_admin.append(url)
            elif url.startswith('/attendance'):
                url_attendance.append(url)
            else:
                url_basic.append(url)
        urls = {'基本':url_basic,'管理员':url_admin,'考勤系统':url_attendance}
        self.render('admin/addrole.html',worker_ids=worker_ids,urls=urls)
    def post(self):
        role_name = self.get_argument('role_name')
        description = self.get_argument('desc')
        urls_can_visit = self.get_arguments('url_selected[]')
        auth_to_workerid = self.get_arguments('worker_id_selected[]')
        oo_r = OrmOperator(auth.Role)
        oo_r.add_row(role_name=role_name,description=description)
        for id in auth_to_workerid:
            oo_ur = OrmOperator(auth.UserRole)
            oo_ur.add_row(role_name=role_name,worker_id=id)
        for url in urls_can_visit:
            oo_rp = OrmOperator(auth.RolePermission)
            oo_rp.add_row(role_name=role_name,url=url)
        self.write('''<script>
                        alert('添加成功');
                        window.location='/admin/addrole'
                    </script>''')
