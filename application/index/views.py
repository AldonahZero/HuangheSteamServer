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

from django.shortcuts import render, redirect

# Create your views here.

from django.utils.decorators import method_decorator
from django.views import View

import application.menu.services
from application.index import services
from application.user.models import User
from config.env import DEBUG
from middleware.login_middleware import check_login
from utils import R

from utils.utils import getImageURL, uid


# 获取系统菜单
@method_decorator(check_login, name='get')
class MenuView(View):
    # 接收GET请求并渲染HTML
    def get(self, request):
        # 获取菜单列表
        menuList = application.menu.services.GetPermissionMenuList(uid(request))
        # 返回结果
        return R.ok(data=menuList)


# 获取用户信息
@method_decorator(check_login, name='get')
class UserView(View):
    # 接收GET请求并渲染HTML
    def get(self, request):
        # 查询用户信息
        user = User.objects.filter(is_delete=False, id=uid(request)).first()
        if not user:
            return R.failed("用户不存在")
        # 获取权限节点列表
        permissionList = application.menu.services.GetPermissionsList(uid(request))
        # 返回用户信息
        info = {
            'realname': user.realname,
            'nickname': user.nickname,
            'avatar': getImageURL(user.avatar),
            'gender': user.gender,
            'mobile': user.mobile,
            'email': user.email,
            'intro': user.intro,
            'address': user.address,
            'roles': [],
            'permissionList': permissionList,
        }
        # 返回结果
        return R.ok(data=info)


# 个人中心
@method_decorator(check_login, name='dispatch')
class UserInfoView(View):
    # 接收GET请求并渲染HTML
    def get(self, request):
        # 用户ID
        user_id = uid(request)
        # 获取当前用户信息
        user = User.objects.filter(is_delete=False, id=user_id).first()
        # 用户头像
        user.avatar = getImageURL(user.avatar)
        # 模板参数
        content = {
            'user': user,
        }
        # 使用render渲染方式
        return render(request, 'user_info/index.html', content)

    # 接收POST请求
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 用户ID
        user_id = uid(request)
        # 调用更新用户服务方法
        result = services.UserInfo(request, user_id)
        # 返回结果
        return result


# 更新密码
@method_decorator(check_login, name='put')
class UpdatePwdView(View):
    # 接收POST请求
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 用户ID
        user_id = uid(request)
        # 调用更新用户服务方法
        result = services.UpdatePwd(request, user_id)
        # 返回结果
        return result


# 退出登录
@method_decorator(check_login, name='get')
class LogoutView(View):
    # 接收GET请求并渲染HTML
    def get(self, request):
        # 返回注销结果
        return R.ok(msg="注册成功")
