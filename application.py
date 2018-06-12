#coding=utf-8
import url
import tornado.web,os

settings = dict(template_path=os.path.join(os.path.dirname(__file__),"templates"),
                static_path=os.path.join(os.path.dirname(__file__),"statics"),
                cookie_secret= "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                login_url="/login",)

application = tornado.web.Application(handlers=url.url,**settings)