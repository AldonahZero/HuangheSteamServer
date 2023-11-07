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

import json
import logging

from application.index import forms
from application.user.models import User
from utils import R, regular, md5


# 更新用户信息
def UserInfo(request, user_id):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.UserForm(dict_data)
    if form.is_valid():
        # 用户姓名
        realname = form.cleaned_data.get('realname')
        # 用户昵称
        nickname = form.cleaned_data.get('nickname')
        # 性别
        gender = form.cleaned_data.get('gender')
        # 手机号
        mobile = form.cleaned_data.get('mobile')
        # 邮箱
        email = form.cleaned_data.get('email')
        # 详细地址
        address = form.cleaned_data.get('address')
        # 个人简介
        intro = form.cleaned_data.get('intro')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询用户
    user = User.objects.filter(is_delete=False, id=user_id).first()
    if not user:
        return R.failed("用户不存在")

    # 对象赋值
    user.realname = realname
    user.nickname = nickname
    user.gender = gender
    user.mobile = mobile
    user.email = email
    user.address = address
    user.intro = intro

    # 更新数据
    user.save()
    # 返回结果
    return R.ok(msg="更新成功")


# 更新密码
def UpdatePwd(request, user_id):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.UpdatePwdForm(dict_data)
    if form.is_valid():
        # 原始密码
        oldPassword = form.cleaned_data.get('oldPassword')
        # 新密码
        newPassword = form.cleaned_data.get('newPassword')
        # 确认新密码
        rePassword = form.cleaned_data.get('rePassword')
        # 两次输入的新密码校验是否相同
        if newPassword != rePassword:
            return R.failed("两次输入的新密码不一致")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询用户
    user = User.objects.filter(is_delete=False, id=user_id).first()
    if not user:
        return R.failed("用户不存在")

    # 密码MD5加密
    oldPassword = md5.getPassword(oldPassword)
    # 判断原始密码是否正确
    if oldPassword != user.password:
        return R.failed("原始密码不正确")

    # 加密新密码
    password = md5.getPassword(newPassword)

    # 对象赋值
    user.password = password

    # 更新数据
    user.save()
    # 返回结果
    return R.ok(msg="更新成功")
