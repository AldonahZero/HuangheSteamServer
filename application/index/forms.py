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

from application.user import models


# 用户基本信息
class UserForm(forms.ModelForm):
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
    # 手机号
    mobile = forms.CharField(
        max_length=30,
        error_messages={
            'required': '手机号不能为空',
            'max_length': '手机号长度不得超过30个字符',
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
    # 详细地址
    address = forms.CharField(
        max_length=255,
        error_messages={
            'required': '详细地址不能为空',
            'max_length': '详细地址长度不得超过255个字符',
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

    class Meta:
        # 绑定模型
        model = models.User
        # 指定部分字段验证
        fields = ['realname', 'nickname', 'gender', 'mobile', 'email', 'address', 'intro']


# 更新密码
class UpdatePwdForm(forms.ModelForm):
    # 原始密码
    oldPassword = forms.CharField(
        min_length=6,
        max_length=12,
        error_messages={
            'required': '原始密码不能为空',
            'min_length': '原始密码长度为6~12个字符',
            'max_length': '原始密码长度为6~12个字符',
        }
    )
    # 新密码
    newPassword = forms.CharField(
        min_length=6,
        max_length=12,
        error_messages={
            'required': '新密码不能为空',
            'min_length': '新密码长度为6~12个字符',
            'max_length': '新密码长度为6~12个字符',
        }
    )
    # 确认新密码
    rePassword = forms.CharField(
        min_length=6,
        max_length=12,
        error_messages={
            'required': '确认新密码不能为空',
            'min_length': '确认新密码长度为6~12个字符',
            'max_length': '确认新密码长度为6~12个字符',
        }
    )

    class Meta:
        # 绑定模型
        model = models.User
        # 指定部分字段验证
        fields = ['oldPassword', 'newPassword', 'rePassword']
