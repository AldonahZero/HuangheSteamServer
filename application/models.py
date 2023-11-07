from django.db import models


# 基类模型
class BaseModel(models.Model):
    # 主键ID
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='主键ID'
    )
    # 创建人
    create_user = models.IntegerField(
        default=0,
        verbose_name='创建人'
    )
    # 创建时间
    create_time = models.DateTimeField(
        null=True,
        auto_now_add=True,
        verbose_name="创建时间",
        max_length=11
    )
    # 更新人
    update_user = models.IntegerField(
        default=0,
        verbose_name='更新人'
    )
    # 更新时间
    update_time = models.DateTimeField(
        null=True,
        auto_now=True,
        verbose_name="更新时间",
        max_length=11
    )
    # 有效标识：1删除 0正常
    is_delete = models.BooleanField(
        default=0,
        verbose_name="逻辑删除"
    )

    class Meta:
        # 定义前模版为抽象模型类，用于其他模版继承，数据库迁移不会创建BaseModel表
        abstract = True
