import tornado.web
from .basehandler import BaseHandler

class IndexAllHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html',worker_id=self.get_secure_cookie("worker_id").split(b':')[0])
