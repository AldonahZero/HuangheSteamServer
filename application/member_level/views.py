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

from django.shortcuts import render

# Create your views here.


from django.utils.decorators import method_decorator
from django.views import View

from application.member_level import services
from config.env import DEBUG
from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired

# 渲染会员等级首页
from utils import R


# 查询会员等级分页数据
@method_decorator(check_login, name="get")
class MemberLevelListView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:memberlevel:list",)

    # 接收GET请求
    def get(self, request):
        # 调用查询会员等级分页数据方法
        result = services.MemberLevelList(request)
        # 返回结果
        return result


# 查询会员等级详情
@method_decorator(check_login, name="get")
class MemberLevelDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:memberlevel:detail",)

    # GET请求渲染HTML模板
    def get(self, request, member_level_id):
        # 调用查询会员等级详情服务方法
        data = services.MemberLevelDetail(member_level_id)
        # 返回结果
        return R.ok(data=data)


# 添加会员等级
@method_decorator(check_login, name="post")
class MemberLevelAddView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ("sys:memberlevel:add",)

    # 接收POST请求
    def post(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用添加会员等级服务方法
        result = services.MemberLevelAdd(request)
        # 返回结果
        return result


# 更新会员等级
@method_decorator(check_login, name="put")
class MemberLevelUpdateView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:memberlevel:update',)

    # 接收PUT请求
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新会员等级服务方法
        result = services.MemberLevelUpdate(request)
        # 返回结果
        return result


# 删除会员等级
@method_decorator(check_login, name="delete")
class MemberLevelDeleteView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:memberlevel:delete',)

    # 接收DELETE请求
    def delete(self, request, member_level_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除会员等级服务方法
        result = services.MemberLevelDelete(member_level_id)
        # 返回结果
        return result


# 获取会员等级列表
@method_decorator(check_login, name="get")
class GetMemberLevelList(View):
    # 接收GET请求
    def get(self, request):
        # 调用查询会员等级列表服务方法
        data = services.GetMemberLevelList()
        # 返回结果
        return R.ok(data=data)
