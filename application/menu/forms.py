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

from application.menu import models


# 菜单表单验证
class MenuForm(forms.ModelForm):
    # 菜单标题
    title = forms.CharField(
        max_length=150,
        error_messages={
            'required': '菜单标题不能为空',
            'max_length': '菜单标题长度不得超过150个字符',
        }
    )
    # 菜单图标
    icon = forms.CharField(
        required=False,
        max_length=50,
        error_messages={
            'required': '菜单图标不能为空',
            'max_length': '菜单图标长度不得超过50个字符',
        }
    )
    # 路由地址
    path = forms.CharField(
        max_length=255,
        error_messages={
            'required': '路由地址不能为空',
            'max_length': '路由地址长度不得超过255个字符',
        }
    )
    # 组件路径
    component = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '组件路径不能为空',
            'max_length': '组件路径长度不得超过255个字符',
        }
    )

    # 上级ID
    parent_id = forms.IntegerField(
        min_value=0,
        error_messages={
            'min_value': '上级菜单ID不能小于0'
        }
    )
    # 菜单类型：0-菜单 1-节点
    type = forms.IntegerField(
        min_value=0,
        max_value=1,
        error_messages={
            'required': '菜单类型不能为空',
            'min_value': '菜单类型值在0~1之间',
            'max_value': '菜单类型值在0~1之间',
        }
    )
    # 打开方式：1-内部打开 2-外部打开
    target = forms.CharField(
        max_length=30,
        error_messages={
            'required': '打开方式不能为空',
            'max_length': '打开方式长度不得超过30个字符',
        }
    )
    # 权限节点
    permission = forms.CharField(
        required=False,
        max_length=150,
        error_messages={
            'required': '权限节点不能为空',
            'max_length': '权限节点长度不得超过150个字符',
        }
    )
    # 是否可见：0-可见 2-不可见
    hide = forms.IntegerField(
        min_value=0,
        max_value=1,
        error_messages={
            'required': '是否可见不能为空',
            'min_value': '是否可见值在0~1之间',
            'max_value': '是否可见值在0~1之间',
        }
    )
    # 菜单状态：1-正常 2-禁用
    status = forms.IntegerField(
        min_value=1,
        max_value=2,
        error_messages={
            'required': '菜单状态不能为空',
            'min_value': '菜单状态值在1~2之间',
            'max_value': '菜单状态值在1~2之间',
        }
    )
    # 菜单排序
    sort = forms.IntegerField(
        min_value=0,
        max_value=99999,
        error_messages={
            'required': '菜单排序不能为空',
            'min_value': '菜单排序值在0~99999之间',
            'max_value': '菜单排序值在0~99999之间',
        }
    )
    # 菜单备注
    note = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'max_length': '菜单备注长度不能大于255个字符'
        }
    )
    # 菜单节点
    checked_list = forms.Field(
        required=False,
        error_messages={
            'required': '菜单节点不能为空',
        }
    )

    class Meta:
        # 绑定模型
        model = models.Menu
        # 指定部分字段验证
        fields = ['title', 'icon', 'path', 'component', 'parent_id', 'type', 'target', 'permission', 'hide', 'status',
                  'sort', 'note', 'checked_list']
