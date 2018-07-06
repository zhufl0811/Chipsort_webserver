from .basehandler import BaseHandler

class LogoutHandler(BaseHandler):
    def prepare(self):
        pass
    def get(self):
        self.clear_all_cookies()
        self.write('''<script>
                        alert('注销成功');
                        window.location='/login'
                    </script>''')
    def on_finish(self):
        pass