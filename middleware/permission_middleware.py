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

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render

import application.menu.services

from utils import R


# 鉴权中间件
from utils.utils import uid


class PermissionRequired(PermissionRequiredMixin):

    def has_permission(self):
        # 获取方法节点权限标识
        permissions = self.get_permission_required()
        # 用户ID
        user_id = uid(self.request)
        if user_id != 1:
            # 获取用户权限节点
            permission_list = application.menu.services.GetPermissionsList(user_id)
            for permission in permissions:
                if permission not in permission_list:
                    # 无节点权限，禁止放行
                    return False
        # 直接放行
        return True

    # 没有权限时候的报错回调
    def handle_no_permission(self):
        if self.request.path.find('index') != -1:
            return render(self.request, '403.html')
        else:
            return R.failed("暂无操作权限")
