# coding = utf-8
import tornado.ioloop
import tornado.options
import tornado.httpserver
from application import application
from tornado.options import define,options

define("port",default = 8000,help = "run on the given port",type=int)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	print("Development server is running at http://127.0.0.1:%s\n" % options.port+
		  '考勤管理首页：http://127.0.0.1:%s/attendance\n'% options.port+
          '用户登陆：http://127.0.0.1:%s/login'%options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__=="__main__":
	main()