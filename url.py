import os
from handlers.attendance.index import IndexAttHandler
from handlers.attendance.workarrangement_type import WaTypeHandler
from handlers.login import LoginHandler
from handlers.index import IndexAllHandler
from handlers.admin.index import AdminIndexHandler
from handlers.admin.addper import AddPerHandler
from handlers.admin.delper import DelPerHandler
from handlers.admin.adduser import AddUserHandler
from handlers.admin.deluser import DelUserHandler
from handlers.admin.addrole import AddRoleHandler
from handlers.admin.delrole import DelRoleHandler
from handlers.admin.editper import EditPerHandler
from handlers.admin.edituser import EditUserHandler
from handlers.admin.editrole import EditRoleHandler
from handlers.logout import LogoutHandler
from handlers.attendance.workday import WorkDayHandler
from tornado.web import StaticFileHandler
from handlers.attendance.work_arrangement import WorkArrangementHandler
from handlers.attendance.workarrangement_query import WAQueryHandler
from handlers.attendance.overtime_submit import OverTimeSubmitHandler
from handlers.attendance.overtime_audit import OverTimeAuditHandler
from handlers.attendance.overtime_query import OverTimeQueryHandler
from handlers.attendance.vacation_submit import VacationSubmitHandler
from handlers.attendance.vacation_audit import VacationAuditHandler
from handlers.attendance.vacation_query import VacationQueryHandler

current_path = os.path.join(os.path.dirname(__file__))

url = [(r'/attendance',IndexAttHandler),
       (r'/login',LoginHandler),
       (r'/',IndexAllHandler),
       (r'/attendance/workarrangement',WorkArrangementHandler),
       (r'/admin',AdminIndexHandler),
       (r'/admin/addper',AddPerHandler),
       (r'/admin/delper',DelPerHandler),
       (r'/admin/adduser',AddUserHandler),
       (r'/admin/deluser',DelUserHandler),
       (r'/admin/addrole',AddRoleHandler),
       (r'/admin/delrole',DelRoleHandler),
       (r'/admin/editrole',EditRoleHandler),
       (r'/admin/edituser(.*?)',EditUserHandler),
       (r'/admin/editper',EditPerHandler),
       (r'/logout',LogoutHandler),
       (r'/attendance/workarrangement_type',WaTypeHandler),
       (r'/attendance/workday',WorkDayHandler),
       (r'/attendance/workarrangement_query',WAQueryHandler),
       (r'/attendance/overtime_submit',OverTimeSubmitHandler),
       (r'/attendance/overtime_audit',OverTimeAuditHandler),
       (r'/attendance/overtime_query',OverTimeQueryHandler),
       (r'/attendance/vacation_submit',VacationSubmitHandler),
       (r'/attendance/vacation_audit',VacationAuditHandler),
       (r'/attendance/vacation_query',VacationQueryHandler),
       (r'^/attendance/(.*?)$',StaticFileHandler,{"path":os.path.join(current_path, "templates/attendance")}),
       (r'^/statics/(.*?)$', StaticFileHandler, {"path": os.path.join(current_path, "statics")})
       ]