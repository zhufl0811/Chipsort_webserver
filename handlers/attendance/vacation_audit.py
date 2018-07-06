import tornado.web
from ..basehandler import BaseHandler

class VacationAuditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass
    def post(self):
        pass