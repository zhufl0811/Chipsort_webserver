from .basehandler import BaseHandler
from models.auth import User
from methods.psd_to_md5 import psd_to_md5
from methods.ormoperator import OrmOperator


class LoginHandler(BaseHandler):
    def prepare(self):
        pass
    def get(self):
        self.render('login.html')
    def post(self):
        worker_id = self.get_argument('worker_id')
        psd_entried = psd_to_md5(self.get_argument('psd'))
        oo_U = OrmOperator(User)
        psd_indatabase = oo_U.query_all('psd',worker_id=worker_id)
        if psd_entried == psd_indatabase[0]:
            self.set_secure_cookie("worker_id", worker_id,expires_days=None)
            self.redirect('/')
        else:
            self.write('/login')
