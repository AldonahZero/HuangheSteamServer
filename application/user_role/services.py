from application.user_role.models import UserRole


# 根据用户ID查询角色列表
def getUserRoleList(userId):
    sql = 'SELECT r.* FROM django_role AS r '
    sql += 'INNER JOIN django_user_role AS ur ON r.id=ur.role_id '
    sql += 'WHERE ur.user_id=%s AND r.is_delete=0'
    list = UserRole.objects.raw(sql, [userId])
    # 实例化角色列表
    role_list = []
    if list:
        for v in list:
            item = {
                'id': v.id,
                'name': v.name,
            }
            # 加入数组
            role_list.append(item)
    # 返回结果
    return role_list
