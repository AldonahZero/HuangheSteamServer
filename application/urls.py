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

"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登录页
    path('', include('application.login.urls')),
    # 系统主页
    path('index/', include('application.index.urls')),
    # 文件上传
    path('upload/', include('application.upload.urls')),
    # 使用include函数，level.urls为业务模块里的urls包
    # 职级总路由
    path('level/', include('application.level.urls')),
    # 岗位总路由
    path('position/', include('application.position.urls')),
    # 部门总路由
    path('dept/', include('application.dept.urls')),
    # 角色总路由
    path('role/', include('application.role.urls')),
    # 角色菜单总路由
    path('rolemenu/', include('application.role_menu.urls')),
    # 城市总路由
    path('city/', include('application.city.urls')),
    # 站点总路由
    path('item/', include('application.item.urls')),
    # 栏目总路由
    path('itemcate/', include('application.item_cate.urls')),
    # 友链总路由
    path('link/', include('application.link.urls')),
    # 广告位总路由
    path('adsort/', include('application.ad_sort.urls')),
    # 广告总路由
    path('ad/', include('application.ad.urls')),
    # 会员等级总路由
    path('memberlevel/', include('application.member_level.urls')),
    # 会员总路由
    path('member/', include('application.member.urls')),
    # 通知公告总路由
    path('notice/', include('application.notice.urls')),
    # 用户总路由
    path('user/', include('application.user.urls')),
    # 字典总路由
    path('dict/', include('application.dict.urls')),
    # 字典项总路由
    path('dictdata/', include('application.dict_data.urls')),
    # 配置总路由
    path('config/', include('application.config.urls')),
    # 配置项总路由
    path('configdata/', include('application.config_data.urls')),
    # 菜单总路由
    path('menu/', include('application.menu.urls')),
    # 网站配置总路由
    path('configweb/', include('application.config_web.urls')),
]
