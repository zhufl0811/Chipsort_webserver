import tornado.web
from ..basehandler import BaseHandler

class IndexAttHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('attendance/index.html',worker_id=self.get_secure_cookie("worker_id"))