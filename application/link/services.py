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

from application.constants import LINK_TYPE_LIST, LINK_PLATFORM_LIST, LINK_FORM_LIST
from application.link import forms
from application.link.models import Link
from constant.constants import PAGE_LIMIT
from utils import R, regular
from utils.utils import getImageURL, saveImage, uid


# 查看友链分页数据
def LinkList(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Link.objects.filter(is_delete=False)
    # 友链名称模糊筛选
    name = request.GET.get('name')
    if name:
        query = query.filter(name__contains=name)
    # 友链类型：1友情链接 2合作伙伴
    type = request.GET.get('type')
    if type:
        query = query.filter(type=type)
    # 投放平台：1PC站 2WAP站 3微信小程序 4APP应用
    platform = request.GET.get('platform')
    if platform:
        query = query.filter(platform=platform)
    # 友链形式：1文字链接 2图片链接
    form = request.GET.get('form')
    if form:
        query = query.filter(form=form)
    # 状态筛选
    status = request.GET.get('status')
    if status:
        query = query.filter(status=status)
    # 排序
    query = query.order_by("sort")
    # 设置分页
    paginator = Paginator(query, limit)
    # 记录总数
    count = paginator.count
    # 分页查询
    link_list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(link_list) > 0:
        for item in link_list:
            data = {
                'id': item.id,
                'name': item.name,
                'type': item.type,
                'type_name': LINK_TYPE_LIST.get(item.type),
                'url': item.url,
                'item_id': item.item_id,
                'cate_id': item.cate_id,
                'platform': item.platform,
                'platform_name': LINK_PLATFORM_LIST.get(item.platform),
                'form': item.form,
                'form_name': LINK_FORM_LIST.get(item.form),
                'image': getImageURL(item.image),
                'status': item.status,
                'note': item.note,
                'sort': item.sort,
                'create_time': str(item.create_time.strftime('%Y-%m-%d %H:%M:%S')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d %H:%M:%S')) if item.update_time else None,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


# 根据ID查看友链详情
def LinkDetail(link_id):
    # 根据ID查询友链
    link = Link.objects.filter(is_delete=False, id=link_id).first()
    # 查询结果为空判断
    if not link:
        return None
    # 声明结构体
    data = {
        'id': link.id,
        'name': link.name,
        'type': link.type,
        'url': link.url,
        'platform': link.platform,
        'form': link.form,
        'image': getImageURL(link.image),
        'status': link.status,
        'note': link.note,
        'sort': link.sort,
    }
    # 返回结果
    return data


# 添加友链
def LinkAdd(request):
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
    form = forms.LinkForm(data=dict_data)
    if form.is_valid():
        # 友链名称
        name = form.cleaned_data.get("name")
        # 友链URL
        url = form.cleaned_data.get("url")
        # 友链类型
        type = int(form.cleaned_data.get("type"))
        # 友链平台
        platform = int(form.cleaned_data.get("platform"))
        # 友链形式
        link_form = int(form.cleaned_data.get("form"))
        # 友链图片
        image = form.cleaned_data.get('image')
        # 图片处理
        if image:
            image = saveImage(image, "link")
        # 友链状态
        status = form.cleaned_data.get('status')
        # 友链备注
        note = form.cleaned_data.get('note')
        # 友链排序
        sort = form.cleaned_data.get('sort')
        # 创建数据
        Link.objects.create(
            name=name,
            url=url,
            type=type,
            platform=platform,
            form=link_form,
            image=image,
            status=status,
            note=note,
            sort=sort,
            create_user=uid(request)
        )
        # 返回结果
        return R.ok(msg="添加成功")
    else:
        # 获取错误描述
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(msg=err_msg)


# 更新友链
def LinkUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 友链ID
        link_id = dict_data.get('id')
        # 友链ID判空
        if not link_id or int(link_id) <= 0:
            return R.failed("友链ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.LinkForm(dict_data)
    if form.is_valid():
        # 友链名称
        name = form.cleaned_data.get("name")
        # 友链URL
        url = form.cleaned_data.get("url")
        # 友链类型
        type = int(form.cleaned_data.get("type"))
        # 友链平台
        platform = int(form.cleaned_data.get("platform"))
        # 友链形式
        link_form = int(form.cleaned_data.get("form"))
        # 友链图片
        image = form.cleaned_data.get('image')
        # 图片处理
        if image:
            image = saveImage(image, "link")
        # 友链状态
        status = form.cleaned_data.get('status')
        # 友链备注
        note = form.cleaned_data.get('note')
        # 友链排序
        sort = form.cleaned_data.get('sort')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询友链
    link = Link.objects.only('id').filter(id=link_id, is_delete=False).first()
    # 查询结果判断
    if not link:
        return R.failed("友链不存在")

    # 对象赋值
    link.name = name
    link.url = url
    link.type = type
    link.platform = platform
    link.form = link_form
    link.image = image
    link.status = status
    link.note = note
    link.sort = sort
    link.update_user = uid(request)
    # 更新数据
    link.save()
    # 返回结果
    return R.ok(msg="更新成功")


# 删除友链
def LinkDelete(link_id):
    # 记录ID为空判断
    if not link_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = link_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            link = Link.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not link:
                return R.failed("友链不存在")
            # 设置删除标识
            link.is_delete = True
            # 更新记录
            link.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))


# 设置状态
def LinkStatus(request):
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
    form = forms.LevelStatusForm(data=dict_data)
    if form.is_valid():
        # 友链ID
        id = int(form.cleaned_data.get('id'))
        # 友链状态
        status = int(form.cleaned_data.get("status"))
    else:
        # 获取错误描述
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(msg=err_msg)

    # 根据ID查询友链
    link = Link.objects.only('id').filter(id=id, is_delete=False).first()
    # 查询结果判空
    if not link:
        return R.failed("记录不存在")
    # 给对象赋值
    link.status = status
    # 更新记录
    link.save()
    # 返回结果
    return R.ok()
