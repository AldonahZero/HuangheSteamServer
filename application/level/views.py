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

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from config.env import DEBUG
from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired
from . import services
from utils import R

# 为全部请求方法添加装饰器
from .models import Level


# 查询职级分页数据
# 为全部请求方法添加装饰器
@method_decorator(check_login, name='dispatch')
class LevelListView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:level:list',)

    # POST查询分页数据
    def get(self, request):
        # 调用查询职级分页数据服务方法
        result = services.LevelList(request)
        # 返回结果
        return result


# 查询职级详情
@method_decorator(check_login, name='dispatch')
class LevelDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:level:detail',)

    # GET请求渲染HTML模板
    def get(self, request, level_id):
        # 调用查询职级详情服务方法
        data = services.LevelDetail(level_id)
        # 返回结果
        return R.ok(data=data)


# 添加职级
@method_decorator(check_login, name='dispatch')
class LevelAddView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:level:add',)

    # 接收POST网络请求
    def post(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用添加职级服务
        result = services.LevelAdd(request)
        # 返回结果
        return result


# 更新职级
@method_decorator(check_login, name='put')
class LevelUpdateView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:level:update',)

    # PUT请求提交数据
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新职级服务方法
        result = services.LevelUpdate(request)
        # 返回结果
        return result


# 删除职级
@method_decorator(check_login, name='dispatch')
class LevelDeleteView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:level:delete',)

    def delete(self, request, level_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除职级服务方法
        result = services.LevelDelete(level_id)
        # 返回结果
        return result


# 设置职级状态
@method_decorator(check_login, name='put')
class LevelStatusView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:level:status',)

    # PUT请求提交数据
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用设置职级状态服务方法
        result = services.LevelStatus(request)
        # 返回结果
        return result


# 导入Excel(此方法为预留接口，暂未开放)
@method_decorator(check_login, name='post')
class LevelImportView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:level:import',)

    # 接收POST请求
    def post(self, request):
        # 预留的接口
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        print("导入数据")
        return R.ok()


# 导出Excel(此方法为预留接口，暂未开放)
@method_decorator(check_login, name='get')
class LevelExportView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:level:export',)

    # 接收GET请求
    def get(self, request):
        # 预留的接口
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        print("导出数据")
        return R.ok()


# 获取职级数据列表
@method_decorator(check_login, name='get')
class LevelGetListView(View):

    # 接收GET请求
    def get(self, request):
        # 调用查询职级数据
        result = services.getLevelList()
        # 返回结果
        return R.ok(data=result)
