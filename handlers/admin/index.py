import tornado.web
from ..basehandler import BaseHandler
from methods.get_all_user_info import get_all_user_info

class AdminIndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_info = get_all_user_info()
        for user in user_info:
            user[2] = '【'+'】，【'.join(user[2].split(','))+'】'
        self.render('admin/index.html',user_info=user_info)