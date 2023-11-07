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

from django.db import models

# Create your models here.
from application.models import BaseModel

from config.env import TABLE_PREFIX


# 会员模型
class Member(BaseModel):
    # 用户姓名
    realname = models.CharField(max_length=150, verbose_name="用户姓名", help_text="用户姓名")
    # 用户昵称
    nickname = models.CharField(max_length=150, verbose_name="用户昵称", help_text="用户昵称")
    # 性别：1-男 2-女 3-保密
    GENDER_CHOICES = (
        (1, "男"),
        (2, "女"),
        (3, "保密"),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1, verbose_name="性别：1-男 2-女 3-保密",
                                 help_text="性别：1-男 2-女 3-保密")
    # 用户头像
    avatar = models.CharField(max_length=255, verbose_name="用户头像", help_text="用户头像")
    # 出生日期
    birthday = models.DateField(max_length=30, verbose_name="出生日期", help_text="出生日期")
    # 邮箱
    email = models.CharField(max_length=50, verbose_name="邮箱", help_text="邮箱")
    # 省份编码
    province_code = models.CharField(max_length=30, verbose_name="省份编码", help_text="省份编码")
    # 城市编码
    city_code = models.CharField(max_length=30, verbose_name="城市编码", help_text="城市编码")
    # 县区编码
    district_code = models.CharField(max_length=30, verbose_name="县区编码", help_text="县区编码")
    # 省市区信息
    address_info = models.CharField(max_length=255, verbose_name="省市区信息", help_text="省市区信息")
    # 详细地址
    address = models.CharField(max_length=255, verbose_name="详细地址", help_text="详细地址")
    # 用户名
    username = models.CharField(max_length=30, verbose_name="用户名", help_text="用户名")
    # 密码
    password = models.CharField(max_length=255, verbose_name="密码", help_text="密码")
    # 会员等级
    member_level = models.IntegerField(default=0, verbose_name="会员等级", help_text="会员等级")
    # 个人简介
    intro = models.CharField(null=True, max_length=255, verbose_name="个人简介", help_text="个人简介")
    # 个人签名
    signature = models.CharField(null=True, max_length=255, verbose_name="个人签名", help_text="个人签名")
    # 注册来源：1-网站注册 2-客户端注册 3-小程序注册 4-手机站注册 5-后台添加
    SOURCE_CHOICES = (
        (1, "网站注册"),
        (2, "客户端注册"),
        (3, "小程序注册"),
        (4, "手机站注册"),
        (5, "后台添加"),
    )
    source = models.IntegerField(choices=SOURCE_CHOICES, default=0,
                                 verbose_name="注册来源：1-网站注册 2-客户端注册 3-小程序注册 4-手机站注册 5-后台添加",
                                 help_text="注册来源：1-网站注册 2-客户端注册 3-小程序注册 4-手机站注册 5-后台添加")
    # 状态
    STATUS_CHOICES = (
        (1, "正常"),
        (2, "禁用"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="状态：1-正常 2-禁用",
                                 help_text="状态：1-正常 2-禁用")

    class Meta:
        # 数据表名
        db_table = TABLE_PREFIX + "member"
        verbose_name = "会员表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "会员{}".format(self.id)
