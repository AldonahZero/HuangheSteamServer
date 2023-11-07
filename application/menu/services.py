# +----------------------------------------------------------------------
# | DjangoAdmin敏捷开发框架 [ 赋能开发者，助力企业发展 ]
# +----------------------------------------------------------------------
# | 版权所有 2021~2023 北京DjangoAdmin研发中心
# +----------------------------------------------------------------------
# | Licensed LGPL-3.0 DjangoAdmin并不是自由软件，未经许可禁止去掉相关版权
# +----------------------------------------------------------------------
# | 官方网站: https://www.djangoadmin.cn
# +----------------------------------------------------------------------
# | 作者: @一米阳光 团队荣誉出品
# +----------------------------------------------------------------------
# | 版权和免责声明:
# | 本团队对该软件框架产品拥有知识产权（包括但不限于商标权、专利权、著作权、商业秘密等）
# | 均受到相关法律法规的保护，任何个人、组织和单位不得在未经本团队书面授权的情况下对所授权
# | 软件框架产品本身申请相关的知识产权，禁止用于任何违法、侵害他人合法权益等恶意的行为，禁
# | 止用于任何违反我国法律法规的一切项目研发，任何个人、组织和单位用于项目研发而产生的任何
# | 意外、疏忽、合约毁坏、诽谤、版权或知识产权侵犯及其造成的损失 (包括但不限于直接、间接、
# | 附带或衍生的损失等)，本团队不承担任何法律责任，本软件框架禁止任何单位和个人、组织用于
# | 任何违法、侵害他人合法利益等恶意的行为，如有发现违规、违法的犯罪行为，本团队将无条件配
# | 合公安机关调查取证同时保留一切以法律手段起诉的权利，本软件框架只能用于公司和个人内部的
# | 法律所允许的合法合规的软件产品研发，详细声明内容请阅读《框架免责声明》附件；
# +----------------------------------------------------------------------

import json
import logging

from application.menu import forms
from application.menu.models import Menu

from utils import R, regular

from utils.utils import uid


# 获取菜单数据
def MenuList(request):
    # 实例化查询对象
    query = Menu.objects.filter(is_delete=False)
    # 菜单标题
    title = request.GET.get('title')
    if title:
        # 菜单标题模糊查询
        query = query.filter(title__contains=title)
    # 查询数据
    list = query.order_by('sort').all()

    # 实例化数组对象
    result = []
    # 遍历数据源
    if list:
        for item in list:
            data = {
                'id': item.id,
                'title': item.title,
                'icon': item.icon,
                'parent_id': item.parent_id,
                'type': item.type,
                'path': item.path,
                'component': item.component,
                'target': item.target,
                'permission': item.permission,
                'status': item.status,
                'hide': item.hide,
                'sort': item.sort,
                'note': item.note,
                'create_time': str(item.create_time.strftime('%Y-%m-%d %H:%M:%S')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d %H:%M:%S')) if item.update_time else None,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result)


# 根据ID查询菜单详情
def MenuDetail(menu_id):
    # 根据ID查询菜单
    menu = Menu.objects.filter(id=menu_id, is_delete=False).first()
    # 查询结果判空
    if not menu:
        return None
    # 查询菜单权限节点
    permission_list = Menu.objects.filter(parent_id=menu_id, type=1, is_delete=False).values()
    # 选中的权限节点
    checked_list = []
    if permission_list:
        for v in permission_list:
            checked_list.append(v['sort'])

    # 实例化结构体
    data = {
        'id': menu.id,
        'title': menu.title,
        'icon': menu.icon,
        'parent_id': menu.parent_id,
        'type': menu.type,
        'path': menu.path,
        'component': menu.component,
        'target': menu.target,
        'permission': menu.permission,
        'status': menu.status,
        'hide': menu.hide,
        'sort': menu.sort,
        'note': menu.note,
        'checked_list': checked_list,
    }
    # 返回结果
    return data


# 添加菜单
def MenuAdd(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数判空
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")

    # 表单验证
    form = forms.MenuForm(data=dict_data)
    if form.is_valid():
        # 菜单标题
        title = form.cleaned_data.get('title')
        # 菜单图标
        icon = form.cleaned_data.get('icon')
        # 上级ID
        parent_id = form.cleaned_data.get('parent_id')
        # 菜单路径
        path = form.cleaned_data.get('path')
        # 菜单组件
        component = form.cleaned_data.get('component')
        # 打开方式
        target = form.cleaned_data.get('target')
        # 权限节点
        permission = form.cleaned_data.get('permission')
        # 菜单类型
        type = form.cleaned_data.get('type')
        # 状态
        status = form.cleaned_data.get('status')
        # 是否隐藏
        hide = form.cleaned_data.get('hide')
        # 菜单排序
        sort = form.cleaned_data.get('sort')
        # 备注
        note = form.cleaned_data.get('note')
        # 权限节点
        checked_list = form.cleaned_data.get('checked_list')
        # 创建数据
        menu = Menu.objects.create(
            title=title,
            icon=icon,
            parent_id=parent_id,
            path=path,
            component=component,
            target=target,
            permission=permission,
            type=type,
            status=status,
            hide=hide,
            sort=sort,
            note=note,
            create_user=uid(request)
        )

        # 保存节点数据
        setPermission(type, checked_list, title, path, menu.id, uid(request))

        # 返回结果
        return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)


# 更新菜单
def MenuUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数判空
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 菜单ID
        menu_id = dict_data.get('id')
        # 菜单ID判空
        if not menu_id:
            return R.failed("菜单ID不能为空")
    except Exception as e:
        logging.info("参数错误：\n{}", format(e))
        return R.failed("参数错误")

    # 表单验证
    form = forms.MenuForm(dict_data)
    if form.is_valid():
        # 菜单标题
        title = form.cleaned_data.get('title')
        # 菜单图标
        icon = form.cleaned_data.get('icon')
        # 上级ID
        parent_id = form.cleaned_data.get('parent_id')
        # 菜单路径
        path = form.cleaned_data.get('path')
        # 菜单组件
        component = form.cleaned_data.get('component')
        # 打开方式
        target = form.cleaned_data.get('target')
        # 权限节点
        permission = form.cleaned_data.get('permission')
        # 菜单类型
        type = form.cleaned_data.get('type')
        # 状态
        status = form.cleaned_data.get('status')
        # 是否隐藏
        hide = form.cleaned_data.get('hide')
        # 菜单排序
        sort = form.cleaned_data.get('sort')
        # 备注
        note = form.cleaned_data.get('note')
        # 权限节点
        checked_list = form.cleaned_data.get('checked_list')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询菜单
    menu = Menu.objects.only('id').filter(id=menu_id, is_delete=False).first()
    # 查询结果判空
    if not menu:
        return R.failed("菜单不存在")

    # 对象赋值
    menu.title = title
    menu.icon = icon
    menu.parent_id = parent_id
    menu.path = path
    menu.component = component
    menu.target = target,
    menu.permission = permission
    menu.type = type
    menu.status = status
    menu.hide = hide
    menu.sort = sort
    menu.note = note
    menu.update_user = uid(request)
    # 更新数据
    menu.save()

    # 保存节点数据
    setPermission(type, checked_list, title, path, menu.id, uid(request))

    # 返回结果
    return R.ok(msg="更新成功")


# 删除菜单
def MenuDelete(menu_id):
    # 记录ID为空判断
    if not menu_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = menu_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            menu = Menu.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not menu:
                return R.failed("菜单不存在")
            # 设置删除标识
            menu.is_delete = True
            # 更新记录
            menu.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))


# 保存节点数据
def setPermission(menu_type, checked_list, name, path, parent_id, user_id):
    # 参数判空
    if menu_type != 0 or checked_list == None or path == "":
        return
    # 删除现有节点
    Menu.objects.filter(is_delete=False, parent_id=parent_id).delete()
    # 模块名称
    moduleTitle = name.replace("管理", "")
    # 请求path处理
    pathArr = path.split('/')
    if len(pathArr) < 3:
        return
    # 模块名
    moduleName = pathArr[len(pathArr) - 2]
    # 遍历数据源
    for v in checked_list:
        # 实例化菜单对象
        entity = Menu()
        # 节点值
        value = int(v)
        if value == 1:
            # 查询
            entity.title = "查询" + moduleTitle
            entity.path = "/" + moduleName + "/list"
            entity.permission = "sys:" + moduleName + ":list"
        elif value == 5:
            # 添加
            entity.title = "添加" + moduleTitle
            entity.path = "/" + moduleName + "/add"
            entity.permission = "sys:" + moduleName + ":add"
        elif value == 10:
            # 修改
            entity.title = "修改" + moduleTitle
            entity.path = "/" + moduleName + "/update"
            entity.permission = "sys:" + moduleName + ":update"
        elif value == 15:
            # 删除
            entity.title = "删除" + moduleTitle
            entity.path = "/" + moduleName + "/delete"
            entity.permission = "sys:" + moduleName + ":delete"
        elif value == 20:
            # 详情
            entity.title = moduleTitle + "详情"
            entity.path = "/" + moduleName + "/detail"
            entity.permission = "sys:" + moduleName + ":detail"
        elif value == 25:
            # 设置状态
            entity.title = "设置状态"
            entity.path = "/" + moduleName + "/status"
            entity.permission = "sys:" + moduleName + ":status"
        elif value == 30:
            # 批量删除
            entity.title = "批量删除"
            entity.path = "/" + moduleName + "/dall"
            entity.permission = "sys:" + moduleName + ":dall"
        elif value == 35:
            # 添加子级
            entity.title = "添加子级"
            entity.path = "/" + moduleName + "/addz"
            entity.permission = "sys:" + moduleName + ":addz"
        elif value == 40:
            # 全部展开
            entity.title = "全部展开"
            entity.path = "/" + moduleName + "/expand"
            entity.permission = "sys:" + moduleName + ":expand"
        elif value == 45:
            # 全部折叠
            entity.title = "全部折叠"
            entity.path = "/" + moduleName + "/collapse"
            entity.permission = "sys:" + moduleName + ":collapse"
        elif value == 50:
            # 导出数据
            entity.title = "导出" + moduleTitle
            entity.path = "/" + moduleName + "/export"
            entity.permission = "sys:" + moduleName + ":export"
        elif value == 55:
            # 导入数据
            entity.title = "导入" + moduleTitle
            entity.path = "/" + moduleName + "/import"
            entity.permission = "sys:" + moduleName + ":import"
        elif value == 60:
            # 分配权限
            entity.title = "分配权限"
            entity.path = "/" + moduleName + "/permission"
            entity.permission = "sys:" + moduleName + ":permission"
        elif value == 65:
            # 重置密码
            entity.title = "重置密码"
            entity.path = "/" + moduleName + "/resetPwd"
            entity.permission = "sys:" + moduleName + ":resetPwd"

        # 设置默认值
        entity.parent_id = parent_id
        entity.type = 1
        entity.status = 1
        entity.target = "_self"
        entity.sort = value
        entity.create_user = user_id
        # 插入数据
        entity.save()


# 获取用户权限节点
def GetPermissionsList(user_id):
    if user_id == 1:
        # 超级管理员
        list = Menu.objects.filter(is_delete=False, type=1).values()
        permission_list = []
        if list:
            for item in list:
                permission_list.append(item['permission'])
        # 返回结果
        return permission_list
    else:
        # 其他用户
        sql = 'SELECT m.* FROM django_menu AS m '
        sql += 'INNER JOIN django_role_menu AS rm ON m.id=rm.menu_id '
        sql += 'INNER JOIN django_user_role AS ur ON ur.role_id=rm.role_id '
        sql += 'WHERE ur.user_id=%s AND (m.type=1 OR (m.type=0 AND m.permission!="")) AND m.`status`=1 AND m.is_delete=0'
        list = Menu.objects.raw(sql, [user_id])
        permission_list = []
        if list:
            for item in list:
                permission_list.append(item.permission)
        # 返回结果
        return permission_list


# 根据用户ID查询菜单列表
def GetPermissionMenuList(user_id):
    if user_id == 1:
        # 超级管理员
        # 查询全部菜单列表
        list = Menu.objects.filter(is_delete=False, status=1, type=0).order_by("sort")
        menu_list = GetTreeList(list)
        return menu_list
    else:
        # 其他用户
        sql = 'SELECT m.* FROM django_menu AS m '
        sql += 'INNER JOIN django_role_menu AS rm ON m.id=rm.menu_id '
        sql += 'INNER JOIN django_user_role AS ur ON ur.role_id=rm.role_id '
        sql += 'WHERE ur.user_id=%s AND m.type=0 AND m.`status`=1 AND m.is_delete=0 '
        sql += 'ORDER BY m.sort ASC;'
        list = Menu.objects.raw(sql, [user_id])
        menu_list = GetTreeList(list)
        return menu_list


# 根据数据源获取树状结构
def GetTreeList(list):
    # 实例化数组
    menu_list = []
    if list:
        for item in list:
            data = {
                'id': item.id,
                'title': item.title,
                'icon': item.icon,
                'path': item.path,
                'parent_id': item.parent_id,
                'type': item.type,
                'component': item.component,
                'permission': item.permission,
                'target': item.target,
                'hide': item.hide,
            }
            menu_list.append(data)
    # 处理数据源为树状结构
    result = get_tree(menu_list, 0)
    # 返回结果
    return result


# 获取树状结构
def get_tree(data, parent_id):
    result = []
    for item in data:
        if parent_id != item["parent_id"]:
            continue
        # 递归调用
        temp = get_tree(data, item["id"])
        if (len(temp) > 0):
            item["children"] = temp
        else:
            item["children"] = []
        # 加入数组
        result.append(item)
    # 返回结果
    return result
