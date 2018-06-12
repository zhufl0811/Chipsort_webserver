from models.auth import *
from methods.ormoperator import OrmOperator
def permission_detect(worker_id):
    oo_ur = OrmOperator(UserRole)
    role_ownby_this_id = oo_ur.query_all('role_name',worker_id=worker_id)

    url_thisid_can_visit = []
    for role in role_ownby_this_id:
        oo_rp = OrmOperator(RolePermission)
        rp_objs=oo_rp.query_all('url',role_name=role)
        url_thisid_can_visit.extend(rp_objs)
    url_thisid_can_visit=list(set(url_thisid_can_visit))
    return url_thisid_can_visit

if __name__ == '__main__':
    print(permission_detect('s777'))