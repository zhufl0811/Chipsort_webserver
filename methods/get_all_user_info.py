from methods.ormoperator import OrmOperator
from models.auth import *

def get_all_user_info():
    oo_u = OrmOperator(User)
    worker_ids = oo_u.query_all('worker_id')
    user_info = []
    for id in worker_ids:
        oo_ur = OrmOperator(UserRole)
        role_names = oo_ur.query_all('role_name', worker_id = id)
        urls = []
        for role_name in role_names:
            oo_rp = OrmOperator(RolePermission)
            url = oo_rp.query_all('url', role_name = role_name)
            urls.extend(url)
        urls = list(set(urls))
        user_info.append([id, ','.join(role_names), ','.join(urls)])
    return user_info

def get_all_role_info():
    oo_u = OrmOperator(Role)
    role_name = oo_u.query_all('role_name')
    role_info=[]
    for role in role_name:
        oo_ur = OrmOperator(UserRole)
        worker_id = oo_ur.query_all('worker_id', role_name=role)
        oo_rp = OrmOperator(RolePermission)
        url = oo_rp.query_all('url', role_name = role)
        role_info.append([role, ','.join(worker_id), ','.join(url)])
    return role_info

if __name__ == '__main__':
    print(get_all_role_info())
