import tornado.web
from methods.permission_detect import permission_detect
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.info import EmployeeInservice

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("worker_id")
    def prepare(self):
        current_url = urlparse(self.request.uri).path
        if current_url in permission_detect(self.get_secure_cookie("worker_id")):
            self.engine = create_engine('mysql+pymysql://root:0811@localhost:3306/chipsort?charset=utf8')
            self.session_class = sessionmaker(bind=self.engine)  # 实例和engine绑定
            self.session = self.session_class()
            self.worker_id=str(self.get_secure_cookie("worker_id"),encoding='utf-8')
            id_name_group=self.session.query(EmployeeInservice.worker_id,EmployeeInservice.name,EmployeeInservice.dep_job).all()
            self.id_name={}
            self.id_group={}
            for i in range(len(id_name_group)):
                self.id_name[id_name_group[i][0].lower()]=id_name_group[i][1]
                self.id_name[id_name_group[i][0].upper()]=id_name_group[i][1]
                self.id_group[id_name_group[i][0].lower()]=id_name_group[i][2]
                self.id_group[id_name_group[i][0].upper()]=id_name_group[i][2]
        else:
            self.send_error(status_code = 403)
    def send_error(self, status_code=500, **kwargs):
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            if status_code==403:
                self.finish("<html><title>403</title>"
                        "<body align='center'><h1>您暂时没有权限访问该网页<h1>"
                           "<h2><a href='/'>返回首页</a></h2>或者<h2><a href='/login'>返回登陆页</a></h2></body></html>" )
    def on_finish(self):
        self.session.close()