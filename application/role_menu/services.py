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

from application.menu.models import Menu
from application.role_menu import forms

from application.role_menu.models import RoleMenu

from utils import R, regular


# 根据角色ID查询菜单列表
def getRoleMenuList(role_id):
    # 获取全部菜单列表
    menuList = Menu.objects.filter(is_delete=False, status=1).order_by("sort").values()
    if len(menuList) == 0:
        return None
    # 根据角色ID查询角色菜单关系数据
    role_menu = RoleMenu.objects.filter(role_id=role_id).values()
    # 菜单ID集合
    idList = []
    # 遍历角色菜单数据源
    if role_menu:
        for v in role_menu:
            # 加入数组
            idList.append(v['menu_id'])

    # 实例化菜单列表
    list = []
    # 遍历菜单数据
    for menu in menuList:
        # 菜单ID
        menu_id = menu['id']
        data = {
            'id': menu_id,
            'title': menu['title'],
            'open': True,
            'parentId': menu['parent_id'],
        }
        if menu_id in idList:
            data['checked'] = True
        # 加入数组
        list.append(data)
    # 返回结果
    return list


# 保存角色菜单数据
def save(request):
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
    form = forms.RoleMenuForm(dict_data)
    if form.is_valid():
        # 角色ID
        role_id = form.cleaned_data.get('roleId')
        # 菜单ID
        menuIdList = form.cleaned_data.get('menuIds')

        # 删除当前角色ID相关菜单权限
        RoleMenu.objects.filter(role_id=role_id).delete()

        # 遍历菜单ID数据源
        if len(menuIdList) > 0:
            for menu_id in menuIdList:
                if menu_id == "":
                    continue
                # 创建角色菜单数据
                RoleMenu.objects.create(
                    role_id=role_id,
                    menu_id=menu_id
                )
        # 返回结果
        return R.ok()
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)
