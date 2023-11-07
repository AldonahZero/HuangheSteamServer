from django import forms

from application.role_menu import models


# 角色菜单表单验证
class RoleMenuForm(forms.ModelForm):
    # 角色ID
    roleId = forms.IntegerField(
        min_value=1,
        error_messages={
            'required': '角色ID不能为空',
            'min_value': '角色ID必须大于0',
        }
    )
    # 菜单ID
    menuIds = forms.Field(
        required=False,
        error_messages={
            'required': '菜单ID不能为空',
        }
    )

    class Meta:
        # 绑定模型
        model = models.RoleMenu
        # 指定字段验证
        fields = ['roleId']
