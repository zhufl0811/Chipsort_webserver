from .basehandler import BaseHandler

class LogoutHandler(BaseHandler):
    def prepare(self):
        pass
    def get(self):
        self.clear_all_cookies()
        self.write('''<head><script>setTimeout("javascript:location.href='/login'", 1500);</script></head>
                                        <h2>注销成功，将跳转到登陆页</h2>''')