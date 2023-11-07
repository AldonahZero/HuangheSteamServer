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

from application.config_data import forms
from application.config_data.models import ConfigData
from application.constants import CONFIG_DATA_TYPE_LIST
from constant.constants import PAGE_LIMIT
from utils import R, regular

# 查询配置项分页数据
from utils.utils import uid


# 查询配置项分页数据
def ConfigDataList(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = ConfigData.objects.filter(is_delete=False)
    # 配置ID
    config_id = request.GET.get('configId', 0)
    query = query.filter(config_id=config_id)
    # 配置项项名称模糊筛选
    title = request.GET.get('title')
    if title:
        query = query.filter(title__contains=title)
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
                'title': item.title,
                'code': item.code,
                'value': item.value,
                'options': item.options,
                'config_id': item.config_id,
                'type': item.type,
                'type_name': CONFIG_DATA_TYPE_LIST.get(item.type),
                'status': item.status,
                'sort': item.sort,
                'note': item.note,
                'create_time': str(item.create_time.strftime('%Y-%m-%d %H:%M:%S')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d %H:%M:%S')) if item.update_time else None,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


# 根据ID查询配置项详情
def ConfigDataDetail(config_id):
    # 根据ID查询配置项
    config = ConfigData.objects.filter(is_delete=False, id=config_id).first()
    # 查询结果判空
    if not config:
        return None
    # 声明结构体
    data = {
        'id': config.id,
        'title': config.title,
        'code': config.code,
        'value': config.value,
        'options': config.options,
        'config_id': config.config_id,
        'type': config.type,
        'status': config.status,
        'sort': config.sort,
        'note': config.note,
    }
    # 返回结果
    return data


# 添加配置项
def ConfigDataAdd(request):
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
    form = forms.ConfigDataForm(dict_data)
    if form.is_valid():
        # 配置项标题
        title = form.cleaned_data.get('title')
        # 配置项编码
        code = form.cleaned_data.get('code')
        # 配置项值
        value = form.cleaned_data.get('value')
        # 配置选项
        options = form.cleaned_data.get('options')
        # 配置ID
        config_id = int(form.cleaned_data.get('config_id'))
        # 配置类型
        type = form.cleaned_data.get('type')
        # 配置项排序
        sort = int(form.cleaned_data.get('sort'))
        # 配置项备注
        note = form.cleaned_data.get('note')
        # 创建数据
        ConfigData.objects.create(
            title=title,
            code=code,
            value=value,
            options=options,
            config_id=config_id,
            type=type,
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


# 更新配置项
def ConfigDataUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 配置ID
        id = dict_data.get('id')
        # 配置ID判空
        if not id or int(id) <= 0:
            return R.failed("配置ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.ConfigDataForm(dict_data)
    if form.is_valid():
        # 配置项标题
        title = form.cleaned_data.get('title')
        # 配置项编码
        code = form.cleaned_data.get('code')
        # 配置项值
        value = form.cleaned_data.get('value')
        # 配置选项
        options = form.cleaned_data.get('options')
        # 配置ID
        config_id = int(form.cleaned_data.get('config_id'))
        # 配置类型
        type = form.cleaned_data.get('type')
        # 配置项排序
        sort = int(form.cleaned_data.get('sort'))
        # 配置项备注
        note = form.cleaned_data.get('note')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询配置
    config = ConfigData.objects.only('id').filter(id=id, is_delete=False).first()
    # 查询结果判断
    if not config:
        return R.failed("配置不存在")

    # 对象赋值
    config.title = title
    config.code = code
    config.value = value
    config.options = options
    config.config_id = config_id
    config.type = type
    config.sort = sort
    config.note = note
    config.update_user = uid(request)

    # 更新数据
    config.save()
    # 返回结果
    return R.ok(msg="更新成功")


# 删除配置项
def ConfigDataDelete(config_id):
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
            config = ConfigData.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not config:
                return R.failed("字典项不存在")
            # 设置删除标识
            config.is_delete = True
            # 更新记录
            config.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))


# 设置状态
def ConfigDataStatus(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数判空
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
    except Exception as e:
        logging.info("错误信息：\n{}".format(e))
        return R.failed("参数错误")

    # 表单验证
    form = forms.ConfigDataStatusForm(data=dict_data)
    if form.is_valid():
        # 配置项ID
        id = int(form.cleaned_data.get('id'))
        # 配置项状态
        status = int(form.cleaned_data.get("status"))
    else:
        # 获取错误描述
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(msg=err_msg)

    # 根据ID查询配置项
    config_data = ConfigData.objects.only('id').filter(id=id, is_delete=False).first()
    # 查询结果判空
    if not config_data:
        return R.failed("记录不存在")
    # 给对象赋值
    config_data.status = status
    # 更新记录
    config_data.save()
    # 返回结果
    return R.ok()
