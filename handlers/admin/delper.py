import tornado.web
from ..basehandler import BaseHandler
from models import auth
from methods.ormoperator import OrmOperator

class DelPerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        oo_per = OrmOperator(auth.Permission)
        url_list_get = oo_per.query_all()
        url_list={}
        for url in url_list_get:
            url_list[url.url]=url.description
        self.render('admin/delper.html',url_list=url_list)
    def post(self):
        url_to_deleted=self.get_argument('delete')
        oo_per = OrmOperator(auth.Permission)
        oo_per.delete(url=url_to_deleted)
        oo_RP = OrmOperator(auth.RolePermission)
        oo_RP.delete(url=url_to_deleted)
        self.write('''<script>
                        alert('删除成功');
                        window.location='/admin/delper'
                    </script>''')
