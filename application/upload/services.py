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

import logging
import os
import random
import time

from config.env import TEMP_PATH, IMAGE_URL, ATTACHMENT_PATH
from utils.file import mkdir


# 上传图片
def uploadImage(request):
    # 获取文件对象
    file = request.FILES.get('file')
    # 文件扩展名
    file_ext = os.path.splitext(file.name)[1].lower()
    # file_ext = file.name.split('.')[-1].lower()
    if file_ext not in [".jpeg", ".png", ".gif"]:
        logging.info("文件格式不正确")

    # 定义文件名，年月日时分秒随机数
    file_name = time.strftime('%Y%m%d%H%M%S') + '%05d' % random.randint(0, 100)
    # 重写合成文件名
    file_name = os.path.join(file_name + file_ext)

    # 保存文件
    save_path = TEMP_PATH + "/" + time.strftime('%Y%m%d')
    # 创建存放目录
    mkdir(save_path)
    # 拼接文件路径
    # path = os.path.join(save_path, file_name)
    path = save_path + "/" + file_name
    # 写入文件
    with open(path, 'wb') as f:
        for line in file:
            f.write(line)

    # 文件地址
    file_url = IMAGE_URL + path.replace(ATTACHMENT_PATH, "")
    # 返回结果
    result = {
        'fileName': file.name,
        'fileUrl': file_url,
    }
    # 返回结果
    return result
