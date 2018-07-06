import tornado.web
from ..basehandler import BaseHandler

class VacationQueryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass
    def post(self):
        pass