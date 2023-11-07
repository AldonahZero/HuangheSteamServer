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

from application.item_cate import models


# 栏目表单验证
class ItemCateForm(forms.ModelForm):
    # 栏目名称
    name = forms.CharField(
        max_length=150,
        error_messages={
            'required': '站点名称不能为空',
            'max_length': '站点名称长度不得超过150个字符',
        }
    )
    # 上级ID
    pid = forms.IntegerField(
        min_value=0,
        error_messages={
            'required': '上级ID不能为空',
            'min_value': '上级ID不能小于0'
        }
    )
    # 站点ID
    item_id = forms.IntegerField(
        min_value=1,
        error_messages={
            'required': '站点ID不能为空',
            'min_value': '站点ID必须大于0',
        }
    )
    # 拼音全称
    pinyin = forms.CharField(
        max_length=150,
        error_messages={
            'required': '拼音全称不能为空',
            'max_length': '拼音全称长度不得超过150个字符',
        }
    )
    # 拼音简称
    code = forms.CharField(
        max_length=150,
        error_messages={
            'required': '拼音简称不能为空',
            'max_length': '拼音简称长度不得超过150个字符',
        }
    )
    # 是否有封面：1是 2否
    is_cover = forms.IntegerField(
        min_value=1,
        max_value=2,
        error_messages={
            'required': '是否有封面不能为空',
            'min_value': '是否有封面的值在1~2之间',
            'max_value': '是否有封面的值在1~2之间',
        }
    )
    # 封面
    cover = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '封面不能为空',
            'max_length': '封面长度不得超过255个字符',
        }
    )
    # 栏目状态
    status = forms.IntegerField(
        min_value=1,
        max_value=2,
        error_messages={
            'required': '栏目状态不能为空',
            'min_value': '栏目状态值在1~2之间',
            'max_value': '栏目状态值在1~2之间',
        }
    )
    # 栏目备注
    note = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'max_length': '栏目备注长度不得超过255个字符',
        }
    )
    # 栏目排序
    sort = forms.IntegerField(
        min_value=0,
        max_value=99999,
        error_messages={
            'required': '栏目排序不能为空',
            'min_value': '栏目排序值在0~99999之间',
            'max_value': '栏目排序值在0~99999之间',
        }
    )

    class Meta:
        # 绑定模型
        model = models.ItemCate
        # 指定部分字段验证
        fields = ['name', 'pid', 'item_id', 'pinyin', 'code', 'is_cover', 'cover', 'status', 'note', 'sort']
