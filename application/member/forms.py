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

from django import forms

from application.member import models


# 会员表单验证
class MemberForm(forms.ModelForm):
    # 用户姓名
    realname = forms.CharField(
        max_length=150,
        error_messages={
            'required': '用户姓名不能为空',
            'max_length': '用户姓名长度不得超过150个字符',
        }
    )
    # 用户昵称
    nickname = forms.CharField(
        max_length=150,
        error_messages={
            'required': '用户昵称不能为空',
            'max_length': '用户昵称长度不得超过150个字符',
        }
    )
    # 性别：1-男 2-女 3-保密
    gender = forms.IntegerField(
        min_value=1,
        max_value=3,
        error_messages={
            'required': '性别不能为空',
            'min_value': '性别值在1~3之间',
            'max_value': '性别值在1~3之间',
        }
    )
    # 头像
    avatar = forms.CharField(
        max_length=255,
        error_messages={
            'required': '头像不能为空',
            'max_length': '头像长度不得超过255个字符',
        }
    )
    # 出生日期
    birthday = forms.DateField(
        input_formats=['%Y-%m-%d'],
        error_messages={
            'required': '出生日期不能为空',
        }
    )
    # 邮箱
    email = forms.CharField(
        max_length=30,
        error_messages={
            'required': '邮箱不能为空',
            'max_length': '邮箱长度不得超过30个字符',
        }
    )
    # 行政区划选择
    city = forms.Field(
        error_messages={
            'required': '所在城市不能为空',
        }
    )
    # 详细地址
    address = forms.CharField(
        max_length=255,
        error_messages={
            'required': '详细地址不能为空',
            'max_length': '详细地址长度不得超过255个字符',
        }
    )
    # 用户名
    username = forms.CharField(
        max_length=30,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '用户名长度不得超过30个字符',
        }
    )
    # 密码
    password = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '密码不能为空',
            'max_length': '密码长度不得超过255个字符',
        }
    )
    # 会员等级
    member_level = forms.IntegerField(
        min_value=0,
        error_messages={
            'required': '会员等级不能为空',
            'min_value': '会员等级值不得小于0',
        }
    )
    # 个人简介
    intro = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '个人简介不能为空',
            'max_length': '个人简介长度不得超过255个字符',
        }
    )
    # 个人签名
    signature = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '个人签名不能为空',
            'max_length': '个人签名长度不得超过255个字符',
        }
    )
    # 注册来源：1-网站注册 2-客户端注册 3-小程序注册 4-手机站注册 5-后台添加
    source = forms.IntegerField(
        min_value=1,
        max_value=5,
        error_messages={
            'required': '注册来源不能为空',
            'min_value': '注册来源在1~5之间',
            'max_value': '注册来源在1~5之间',
        }
    )
    # 用户状态：1-正常 2-禁用
    status = forms.IntegerField(
        min_value=1,
        max_value=2,
        error_messages={
            'required': '用户状态不能为空',
            'min_value': '用户状态值在1~2之间',
            'max_value': '用户状态值在1~2之间',
        }
    )

    class Meta:
        # 绑定模型
        model = models.Member
        # 指定部分字段验证
        fields = ['realname', 'nickname', 'gender', 'avatar', 'birthday', 'city', 'address', 'username', 'password',
                  'member_level', 'intro', 'signature', 'source', 'status']


# 会员状态设置
class MemberStatusForm(forms.ModelForm):
    # 会员状态
    id = forms.IntegerField(
        min_value=1,
        error_messages={
            'required': '会员ID不能为空',
            'min_value': '会员ID不能小于或等于0',
        }
    )
    # 会员状态
    status = forms.IntegerField(
        min_value=1,
        max_value=2,
        error_messages={
            'required': '会员状态不能为空',
            'min_value': '会员状态值在1~2之间',
            'max_value': '会员状态值在1~2之间',
        }
    )

    class Meta:
        # 绑定模型
        model = models.Member
        # 指定部分字段验证
        fields = ["id", "status"]
