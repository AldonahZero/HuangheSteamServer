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
from datetime import datetime, timedelta

from captcha.models import CaptchaStore

from application.login import forms
from application.user.models import User
from utils import R, regular, md5

# 用户登录
from utils.jwts import create_token


def Login(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
    except Exception as e:
        logging.info("错误信息：\n{}".format(e))
        return R.failed("参数错误")

    # 表单验证
    form = forms.LoginForm(data=dict_data)
    if form.is_valid():
        # 登录名
        username = form.cleaned_data.get("username")
        # 登录密码
        password = form.cleaned_data.get("password")
        # 验证码
        captcha = form.cleaned_data.get("captcha")
        # 验证码KEY
        idKey = int(form.cleaned_data.get("idKey"))
        # 验证码
        image_code = CaptchaStore.objects.filter(
            id=idKey
        ).first()
        five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        if image_code and five_minute_ago > image_code.expiration.replace(tzinfo=None):
            image_code and image_code.delete()
            return R.failed(msg="验证码过期")
        else:
            if image_code and (
                    image_code.response == captcha
                    or image_code.challenge == captcha
            ):
                image_code and image_code.delete()
            else:
                image_code and image_code.delete()
                return R.failed(msg="图片验证码错误")

        # 根据用户名查询用户信息
        user = User.objects.filter(is_delete=False, username=username).first()
        if not user:
            return R.failed("用户不存在")

        # 密码MD5加密
        md5_pwd = md5.getPassword(password)

        # 比对密码是否相同
        if md5_pwd != user.password:
            return R.failed(msg="密码不正确")
        # 生成TOKEN
        access_token = create_token({"userId": user.id})
        # 返回结果
        return R.ok(msg="登录成功", data={"access_token": access_token})
    else:
        # 获取错误描述
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(msg=err_msg)
