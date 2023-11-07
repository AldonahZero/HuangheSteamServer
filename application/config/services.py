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

from django.core.paginator import Paginator

from application.config import forms
from application.config.models import Config
from constant.constants import PAGE_LIMIT
from utils import R, regular

# 查询配置分页数据
from utils.utils import uid


def ConfigList(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Config.objects.filter(is_delete=False)
    # 配置名称模糊筛选
    name = request.GET.get('name')
    if name:
        query = query.filter(name__contains=name)
    # 排序
    query = query.order_by("sort")
    # 设置分页
    paginator = Paginator(query, limit)
    # 记录总数
    count = paginator.count
    # 分页查询
    config_list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(config_list) > 0:
        for item in config_list:
            data = {
                'id': item.id,
                'name': item.name,
                'sort': item.sort,
                'note': item.note,
                'create_time': str(item.create_time.strftime('%Y-%m-%d %H:%M:%S')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d %H:%M:%S')) if item.update_time else None,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


# 根据ID获取配置详情
def ConfigDetail(config_id):
    # 根据ID查询配置
    config = Config.objects.filter(is_delete=False, id=config_id).first()
    # 查询结果判空
    if not config:
        return None
    # 声明结构体
    data = {
        'id': config.id,
        'name': config.name,
        'sort': config.sort,
        'note': config.note,
    }
    # 返回结果
    return data


# 添加配置
def ConfigAdd(request):
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
    form = forms.ConfigForm(dict_data)
    if form.is_valid():
        # 配置名称
        name = form.cleaned_data.get('name')
        # 配置排序
        sort = form.cleaned_data.get('sort')
        # 配置备注
        note = form.cleaned_data.get('note')
        # 创建数据
        Config.objects.create(
            name=name,
            sort=sort,
            note=note,
            create_user=uid(request)
        )
        # 返回结果
        return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)


# 更新配置
def ConfigUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 配置ID
        config_id = dict_data.get('id')
        # 配置ID判空
        if not config_id or int(config_id) <= 0:
            return R.failed("配置ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.ConfigForm(dict_data)
    if form.is_valid():
        # 配置名称
        name = form.cleaned_data.get('name')
        # 配置排序
        sort = form.cleaned_data.get('sort')
        # 配置备注
        note = form.cleaned_data.get('note')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询配置
    config = Config.objects.only('id').filter(id=config_id, is_delete=False).first()
    # 查询结果判断
    if not config:
        return R.failed("配置不存在")

    # 对象赋值
    config.name = name
    config.sort = sort
    config.note = note
    config.update_user = uid(request)

    # 更新数据
    config.save()
    # 返回结果
    return R.ok(msg="更新成功")


# 删除配置
def ConfigDelete(config_id):
    # 记录ID为空判断
    if not config_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = config_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            config = Config.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not config:
                return R.failed("配置不存在")
            # 设置删除标识
            config.is_delete = True
            # 更新记录
            config.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))
