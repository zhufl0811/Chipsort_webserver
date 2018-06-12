from methods.get_all_user_info import get_all_user_info
import tornado.web
from ..basehandler import BaseHandler
from methods.ormoperator import OrmOperator
from models.auth import User,UserRole

class DelUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_info = get_all_user_info()
        for user in user_info:
            user[2] = '【'+'】，【'.join(user[2].split(','))+'】'
        self.render('admin/deluser.html',user_info=user_info)
    def post(self):
        worker_id = self.get_argument('delete')
        oo_ur = OrmOperator(UserRole)
        if 'admin' in oo_ur.query_all('role_name',worker_id=worker_id):
            self.write('''<head><script>setTimeout("javascript:location.href='/admin/deluser'", 1500);</script></head>
                                        <h2>无法删除管理员，将跳转到之前页</h2>''')
        else:
            oo_u = OrmOperator(User)
            oo_u.delete(worker_id=worker_id)
            oo_ur = OrmOperator(UserRole)
            oo_ur.delete(worker_id=worker_id)
            self.write('''<head><script>setTimeout("javascript:location.href='/admin/deluser'", 1500);</script></head>
                                        <h2>删除成功，将跳转到之前页</h2>''')