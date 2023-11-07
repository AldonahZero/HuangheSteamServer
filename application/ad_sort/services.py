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

from application.ad_sort import forms
from application.ad_sort.models import AdSort
from application.constants import AD_SORT_PLATFORM_LIST
from application.item.models import Item
from application.item_cate.models import ItemCate
from constant.constants import PAGE_LIMIT
from utils import R, regular

# 查询广告位分页数据
from utils.utils import uid


# 获取广告位分页数据
def AdSortList(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = AdSort.objects.filter(is_delete=False)
    # 名称模糊筛选
    name = request.GET.get('name')
    if name:
        query = query.filter(name__contains=name)
    # 投放平台：1PC站 2WAP站 3微信小程序 4APP应用
    platform = request.GET.get('platform')
    if platform:
        query = query.filter(platform=platform)
    # 栏目状态筛选
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
    list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(list) > 0:
        for item in list:
            # 根据站点ID获取站点信息
            itemInfo = Item.objects.filter(is_delete=False, id=item.item_id).first()
            # 根据栏目ID获取栏目信息
            cateInfo = ItemCate.objects.filter(is_delete=False, id=item.cate_id).first()
            data = {
                'id': item.id,
                'name': item.name,
                'item_id': item.item_id,
                'item_name': itemInfo.name if itemInfo else None,
                'cate_id': item.cate_id,
                'cate_name': cateInfo.name if cateInfo else None,
                'platform': item.platform,
                'loc_id': item.loc_id,
                'platform_name': AD_SORT_PLATFORM_LIST.get(item.platform),
                'description': item.description,
                'sort': item.sort,
                'create_time': str(item.create_time.strftime('%Y-%m-%d %H:%M:%S')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d %H:%M:%S')) if item.update_time else None,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


# 根据ID查询广告位详情
def AdSortDetail(adsort_id):
    # 根据ID查询广告位
    adsort = AdSort.objects.filter(is_delete=False, id=adsort_id).first()
    # 查询结果为空判断
    if not adsort:
        return None
    # 声明结构体
    data = {
        'id': adsort.id,
        'name': adsort.name,
        'item_id': adsort.item_id,
        'cate_id': adsort.cate_id,
        'loc_id': adsort.loc_id,
        'platform': adsort.platform,
        'description': adsort.description,
        'sort': adsort.sort,
    }
    # 返回结果
    return data


# 添加广告位
def AdSortAdd(request):
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
    form = forms.AdSortForm(data=dict_data)
    if form.is_valid():
        # 广告位名称
        name = form.cleaned_data.get("name")
        # 站点ID
        item_id = form.cleaned_data.get('item_id')
        # 栏目ID
        cate_id = form.cleaned_data.get('cate_id')
        # 广告位置
        loc_id = form.cleaned_data.get('loc_id')
        # 投放平台
        platform = int(form.cleaned_data.get("platform"))
        # 广告位备注
        description = form.cleaned_data.get('description')
        # 广告位排序
        sort = form.cleaned_data.get('sort')
        # 创建数据
        AdSort.objects.create(
            name=name,
            item_id=item_id,
            cate_id=cate_id,
            loc_id=loc_id,
            platform=platform,
            description=description,
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


# 更新广告位
def AdSortUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 广告位ID
        adsort_id = dict_data.get('id')
        # 广告位ID判空
        if not adsort_id or int(adsort_id) <= 0:
            return R.failed("广告位ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.AdSortForm(dict_data)
    if form.is_valid():
        # 广告位名称
        name = form.cleaned_data.get("name")
        # 站点ID
        item_id = int(form.cleaned_data.get('item_id'))
        # 栏目ID
        cate_id = int(form.cleaned_data.get('cate_id'))
        # 广告位置
        loc_id = int(form.cleaned_data.get('loc_id'))
        # 投放平台
        platform = int(form.cleaned_data.get("platform"))
        # 广告位备注
        description = form.cleaned_data.get('description')
        # 广告位排序
        sort = form.cleaned_data.get('sort')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询广告位
    adsort = AdSort.objects.only('id').filter(id=adsort_id, is_delete=False).first()
    # 查询结果判断
    if not adsort:
        return R.failed("广告位不存在")

    # 对象赋值
    adsort.name = name
    adsort.item_id = item_id
    adsort.cate_id = cate_id
    adsort.loc_id = loc_id
    adsort.platform = platform
    adsort.description = description
    adsort.sort = sort
    adsort.update_user = uid(request)
    # 更新数据
    adsort.save()
    # 返回结果
    return R.ok(msg="更新成功")


# 删除广告位
def AdSortDelete(adsort_id):
    # 记录ID为空判断
    if not adsort_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = adsort_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            adsort = AdSort.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not adsort:
                return R.failed("广告位不存在")
            # 设置删除标识
            adsort.is_delete = True
            # 更新记录
            adsort.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))


# 查询全部广告位列表
def GetAdSortList():
    # 查询全部广告位列表
    list = AdSort.objects.filter(is_delete=False).values()
    # 实例化广告位对象列表
    sortList = []
    if list:
        for v in list:
            item = {
                'id': v['id'],
                'name': v['name'] + "=>" + str(v['loc_id'])
            }
            sortList.append(item)
    # 返回结果
    return sortList


# 获取广告位列表
def GetAdSortList():
    # 查询广告位列表
    list = AdSort.objects.filter(is_delete=False).order_by("sort").values()
    # 实例化数据列表
    result = []
    # 遍历数据源
    for v in list:
        # 字符串拼接
        data = v
        data['description'] = v['description'] + " >> " + str(v['loc_id'])
        # 加入数组
        result.append(data)
    # 返回结果
    return result
