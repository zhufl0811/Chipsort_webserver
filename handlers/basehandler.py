import tornado.web
from methods.permission_detect import permission_detect
from urllib.parse import urlparse

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("worker_id")
    def prepare(self):
        current_url = urlparse(self.request.uri).path
        if current_url in permission_detect(self.get_secure_cookie("worker_id")):
            pass
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