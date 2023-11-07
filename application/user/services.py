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

from django.core.paginator import Paginator

from application.constants import GENDER_LIST
from application.dept.models import Dept
from application.level.models import Level
from application.position.models import Position
from application.user import forms
from application.user.models import User
from application.user_role import services
from application.user_role.models import UserRole
from constant.constants import PAGE_LIMIT
from utils import R, regular, md5

from utils.utils import getImageURL, saveImage, uid


# 查询用户分页数据
def UserList(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = User.objects.filter(is_delete=False)
    # 用户姓名
    realname = request.GET.get('realname')
    if realname:
        query = query.filter(realname__contains=realname)
    # 性别
    gender = request.GET.get('gender')
    if gender:
        query = query.filter(gender=gender)
    # 用户状态
    status = request.GET.get('status')
    if status:
        query = query.filter(status=status)
    # 排序
    query = query.order_by("id")
    # 设置分页
    paginator = Paginator(query, limit)
    # 记录总数
    count = paginator.count
    # 分页查询
    user_list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(user_list) > 0:
        # 查看部门列表
        dept_list = Dept.objects.filter(is_delete=False).values()
        deptList = {}
        if dept_list:
            for dept in dept_list:
                deptList[dept['id']] = dept['name']

        # 查看职级列表
        level_list = Level.objects.filter(is_delete=False).values()
        levelList = {}
        if level_list:
            for level in level_list:
                levelList[level['id']] = level['name']

        # 查看用户列表
        position_list = Position.objects.filter(is_delete=False).values()
        positionList = {}
        if position_list:
            for position in position_list:
                positionList[position['id']] = position['name']
        for item in user_list:
            # 获取用户角色列表
            roleList = services.getUserRoleList(item.id)
            # 城市
            city_list = []
            # 省份编码
            city_list.append(item.province_code)
            # 城市编码
            city_list.append(item.city_code)
            # 县区编码
            city_list.append(item.district_code)
            # 对象
            data = {
                'id': item.id,
                'realname': item.realname,
                'nickname': item.nickname,
                'gender': item.gender,
                'gender_name': GENDER_LIST.get(item.gender),
                'avatar': getImageURL(item.avatar) if item.avatar else "",
                'mobile': item.mobile,
                'email': item.email,
                'birthday': item.birthday,
                'dept_id': item.dept_id,
                'dept_name': deptList.get(item.dept_id) if deptList else None,
                'level_id': item.level_id,
                'level_name': levelList.get(item.level_id) if levelList else None,
                'position_id': item.position_id,
                'position_name': positionList.get(item.position_id) if positionList else None,
                'username': item.username,
                'status': item.status,
                'sort': item.sort,
                'roleList': roleList,
                'city': city_list,
                'create_time': str(item.create_time.strftime('%Y-%m-%d %H:%M:%S')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d %H:%M:%S')) if item.update_time else None,
            }
            # 加入数组
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


# 根据ID查询用户详情
def UserDetail(user_id):
    # 根据ID查询用户
    user = User.objects.filter(is_delete=False, id=user_id).first()
    # 查询结果判空
    if not user:
        return None

    # 获取用户角色数据
    roleList = UserRole.objects.filter(user_id=user.id).values()
    roles = []
    for role in roleList:
        roles.append(int(role['role_id']))

    # 城市编码
    cityList = []
    # 省份编号
    cityList.append(user.province_code)
    # 城市编码
    cityList.append(user.city_code)
    # 县区编码
    cityList.append(user.district_code)

    # 声明结构体
    data = {
        'id': user.id,
        'realname': user.realname,
        'nickname': user.nickname,
        'gender': user.gender,
        'avatar': getImageURL(user.avatar) if user.avatar else "",
        'mobile': user.mobile,
        'email': user.email,
        'birthday': user.birthday,
        'dept_id': user.dept_id,
        'level_id': user.level_id,
        'position_id': user.position_id,
        'username': user.username,
        'province_code': user.province_code,
        'city_code': user.city_code,
        'district_code': user.district_code,
        'address': user.address,
        'intro': user.intro,
        'status': user.status,
        'note': user.note,
        'sort': user.sort,
        'roles': roles,
        'city': cityList,
    }
    # 返回结果
    return data


# 添加用户
def UserAdd(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.UserForm(dict_data)
    if form.is_valid():
        # 用户姓名
        realname = form.cleaned_data.get('realname')
        # 用户昵称
        nickname = form.cleaned_data.get('nickname')
        # 性别
        gender = form.cleaned_data.get('gender')
        # 头像
        avatar = form.cleaned_data.get('avatar')
        if avatar:
            avatar = saveImage(avatar, "user")
        # 手机号
        mobile = form.cleaned_data.get('mobile')
        # 邮箱
        email = form.cleaned_data.get('email')
        # 出生日期
        birthday = form.cleaned_data.get('birthday')
        # 部门ID
        dept_id = form.cleaned_data.get('dept_id')
        # 职级ID
        level_id = form.cleaned_data.get('level_id')
        # 岗位ID
        position_id = form.cleaned_data.get('position_id')
        # 行政区划
        city = form.cleaned_data.get('city')
        # 详细地址
        address = form.cleaned_data.get('address')
        # 用户名
        username = form.cleaned_data.get('username')
        # 密码
        password = form.cleaned_data.get('password')
        # 个人简介
        intro = form.cleaned_data.get('intro')
        # 状态
        status = form.cleaned_data.get('status')
        # 备注
        note = form.cleaned_data.get('note')
        # 排序
        sort = form.cleaned_data.get('sort')
        # 用户角色
        roles = form.cleaned_data.get('roles')

        # 省市区行政编码处理
        if len(city) != 3:
            return R.failed("请选择所在城市")

        # 创建用户
        user = User.objects.create(
            realname=realname,
            nickname=nickname,
            gender=gender,
            avatar=avatar,
            mobile=mobile,
            email=email,
            birthday=birthday,
            dept_id=dept_id,
            level_id=level_id,
            position_id=position_id,
            province_code=city[0],
            city_code=city[1],
            district_code=city[2],
            address=address,
            username=username,
            password=md5.getPassword(password) if password else None,
            intro=intro,
            status=status,
            note=note,
            sort=sort,
            create_user=uid(request)
        )
        # 创建用户角色数据
        addUserRole(user.id, roles)

        # 返回结果
        return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)


# 更新用户
def UserUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 用户ID
        user_id = dict_data.get('id')
        # 用户ID判空
        if not user_id or int(user_id) <= 0:
            return R.failed("用户ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.UserForm(dict_data)
    if form.is_valid():
        # 用户姓名
        realname = form.cleaned_data.get('realname')
        # 用户昵称
        nickname = form.cleaned_data.get('nickname')
        # 性别
        gender = form.cleaned_data.get('gender')
        # 头像
        avatar = form.cleaned_data.get('avatar')
        if avatar:
            avatar = saveImage(avatar, "user")
        # 手机号
        mobile = form.cleaned_data.get('mobile')
        # 邮箱
        email = form.cleaned_data.get('email')
        # 出生日期
        birthday = form.cleaned_data.get('birthday')
        # 部门ID
        dept_id = form.cleaned_data.get('dept_id')
        # 职级ID
        level_id = form.cleaned_data.get('level_id')
        # 岗位ID
        position_id = form.cleaned_data.get('position_id')
        # 行政区划
        city = form.cleaned_data.get('city')
        # 详细地址
        address = form.cleaned_data.get('address')
        # 用户名
        username = form.cleaned_data.get('username')
        # 密码
        password = form.cleaned_data.get('password')
        # 个人简介
        intro = form.cleaned_data.get('intro')
        # 状态
        status = form.cleaned_data.get('status')
        # 备注
        note = form.cleaned_data.get('note')
        # 排序
        sort = form.cleaned_data.get('sort')
        # 用户角色
        roles = form.cleaned_data.get('roles')

        # 省市区行政编码处理
        if len(city) != 3:
            return R.failed("请选择所在城市")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询用户
    user = User.objects.only('id').filter(id=user_id, is_delete=False).first()
    # 查询结果判断
    if not user:
        return R.failed("用户不存在")

    # 对象赋值
    user.realname = realname
    user.nickname = nickname
    user.gender = gender
    user.avatar = avatar
    user.mobile = mobile
    user.email = email
    user.birthday = birthday
    user.dept_id = dept_id
    user.level_id = level_id
    user.position_id = position_id
    user.province_code = city[0]
    user.city_code = city[1]
    user.district_code = city[2]
    user.address = address
    user.username = username
    user.intro = intro
    user.status = status
    user.note = note
    user.sort = sort
    user.update_user = uid(request)

    # 密码存在是MD5加密
    if password:
        user.password = md5.getPassword(password)

    # 更新数据
    user.save()

    # 创建用户角色数据
    addUserRole(user_id, roles)

    # 返回结果
    return R.ok(msg="更新成功")


# 创建用户角色信息
def addUserRole(user_id, roles):
    # 删除用户角色关系数据
    UserRole.objects.filter(user_id=user_id).delete()
    # 创建新的用户角色关系
    if roles:
        for roleId in roles:
            # 为空直接跳过
            if not roleId:
                continue
            UserRole.objects.create(
                user_id=user_id,
                role_id=roleId
            )


# 删除用户
def UserDelete(user_id):
    # 记录ID为空判断
    if not user_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = user_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            user = User.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not user:
                return R.failed("用户不存在")
            # 设置删除标识
            user.is_delete = True
            # 更新记录
            user.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))


# 设置状态
def UserStatus(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数判空
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
    except Exception as e:
        logging.info("错误信息：\n{}".format(e))
        return R.failed("参数错误")

    # 表单验证
    form = forms.UserStatusForm(data=dict_data)
    if form.is_valid():
        # 用户ID
        user_id = int(form.cleaned_data.get('id'))
        # 用户状态
        status = int(form.cleaned_data.get("status"))
    else:
        # 获取错误描述
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(msg=err_msg)

    # 根据ID查询用户
    user = User.objects.only('id').filter(id=user_id, is_delete=False).first()
    # 查询结果判空
    if not user:
        return R.failed("记录不存在")
    # 给对象赋值
    user.status = status
    # 更新记录
    user.save()
    # 返回结果
    return R.ok()


# 重置密码
def UserResetPwd(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 用户ID
        user_id = dict_data.get('id')
        # 用户ID判空
        if not user_id or int(user_id) <= 0:
            return R.failed("用户ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")

    # 根据ID查询用户
    user = User.objects.filter(is_delete=False, id=user_id).first()
    if not user:
        return R.failed("用户不存在")
    # 加密新密码
    password = md5.getPassword("123456")
    # 对象赋值
    user.password = password
    # 更新数据
    user.save()
    # 返回结果
    return R.ok(msg="重置密码成功")
