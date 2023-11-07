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

from application.config.models import Config
from application.config_data.models import ConfigData
from config.env import IMAGE_URL
from utils import R
from utils.utils import getImageURL, saveImage


# 获取配置信息
def getConfigInfo():
    config_list = []
    # 查询配置列表
    configList = Config.objects.filter(is_delete=False).order_by("sort").values()
    if configList:
        # 遍历数据源
        for val in configList:
            # 配置信息
            config = {
                'config_id': val['id'],
                'config_name': val['name']
            }

            # 查询配置数据列表
            dataList = ConfigData.objects.filter(is_delete=False, status=1, config_id=val['id']).order_by(
                "sort").values()
            # 实例化配置数据对象
            data_list = []
            if dataList:
                for v in dataList:
                    # 数据类型
                    type = v['type']

                    data = {}
                    data["id"] = v['id']
                    data["title"] = v['title']
                    data["code"] = v['code']
                    data["value"] = v['value']
                    data["type"] = v['type']

                    if type == "checkbox":
                        # 复选框
                        itemList = []
                        options = v['options'].split(',')
                        if len(options) > 0:
                            for val in options:
                                item = val.split('=')
                                # 选项值
                                value = {
                                    'label': item[1],
                                    'value': item[0],
                                }
                                itemList.append(value)
                        data['optionsList'] = itemList
                        # 选中值
                        data["value"] = v['value'].split(',') if v['value'] else []
                    elif type == "radio":
                        # 单选按钮
                        itemList = {}
                        options = v['options'].split(',')
                        if len(options) > 0:
                            for val in options:
                                item = val.split('=')
                                itemList[item[0]] = item[1]
                        data['optionsList'] = itemList
                    elif type == "select":
                        # 下拉选择
                        itemList = {}
                        options = v['options'].split(',')
                        if len(options) > 0:
                            for val in options:
                                item = val.split('=')
                                itemList[item[0]] = item[1]
                        data['optionsList'] = itemList
                    elif type == "image":
                        # 单图
                        if v['value']:
                            data["value"] = getImageURL(v['value'])
                    elif type == "images":
                        # 多图
                        if v['value']:
                            # 字符串分裂处理
                            list = v['value'].split(',')
                            itemList = []
                            for v in list:
                                image = getImageURL(v)
                                itemList.append(image)
                            # 图片数据
                            data["value"] = itemList
                    # 加入数组
                    data_list.append(data)
            # 设置配置数据列表
            config['data_list'] = data_list
            # 加入配置数据
            config_list.append(config)

    # 返回结果
    return config_list


# 保存配置信息
def saveConfigInfo(request):
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
    # 数据源处理
    if dict_data:
        for key in dict_data:
            # 参数值
            val = dict_data[key]
            # 图片数据
            item = []
            if isinstance(val, list):
                for v in val:
                    if v[:4] == "http" or v[:5] == "https":
                        # 图片地址处理
                        url = saveImage(v, "config")
                        # 加入数组
                        item.append(url)
                    else:
                        # 复选框处理
                        item.append(v)
                val = ','.join(item)
            else:
                # 其他处理
                if val[:4] == "http" or val[:5] == "https":
                    # 图片地址处理
                    val = saveImage(val, "config")

            # 根据编码查询配置项
            config_data = ConfigData.objects.filter(is_delete=False, code=key).first()
            if not config_data:
                continue
            # 设置
            config_data.value = val
            config_data.save()

        # 返回结果
        return R.ok()
