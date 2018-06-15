import tornado.web

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('second')
        self.finish('haha')
        self.write('fffff')
        self.finish('haha')