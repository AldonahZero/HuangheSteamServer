# Generated by Django 4.1.3 on 2023-02-05 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('realname', models.CharField(help_text='用户姓名', max_length=150, verbose_name='用户姓名')),
                ('nickname', models.CharField(help_text='用户昵称', max_length=150, verbose_name='用户昵称')),
                ('gender', models.IntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], default=1, help_text='性别：1-男 2-女 3-保密', verbose_name='性别：1-男 2-女 3-保密')),
                ('avatar', models.CharField(help_text='用户头像', max_length=255, verbose_name='用户头像')),
                ('mobile', models.CharField(help_text='手机号', max_length=30, verbose_name='手机号')),
                ('email', models.CharField(help_text='邮箱', max_length=50, verbose_name='邮箱')),
                ('birthday', models.DateField(help_text='出生日期', max_length=30, verbose_name='出生日期')),
                ('dept_id', models.IntegerField(default=0, help_text='部门ID', verbose_name='部门ID')),
                ('level_id', models.IntegerField(default=0, help_text='职级ID', verbose_name='职级ID')),
                ('position_id', models.IntegerField(default=0, help_text='岗位ID', verbose_name='岗位ID')),
                ('province_code', models.CharField(help_text='省份编码', max_length=30, verbose_name='省份编码')),
                ('city_code', models.CharField(help_text='城市编码', max_length=30, verbose_name='城市编码')),
                ('district_code', models.CharField(help_text='县区编码', max_length=30, verbose_name='县区编码')),
                ('address_info', models.CharField(help_text='省市区信息', max_length=255, verbose_name='省市区信息')),
                ('address', models.CharField(help_text='详细地址', max_length=255, verbose_name='详细地址')),
                ('username', models.CharField(help_text='用户名', max_length=30, verbose_name='用户名')),
                ('password', models.CharField(help_text='密码', max_length=255, verbose_name='密码')),
                ('salt', models.CharField(help_text='加密盐', max_length=30, verbose_name='加密盐')),
                ('intro', models.CharField(help_text='个人简介', max_length=255, null=True, verbose_name='个人简介')),
                ('status', models.IntegerField(choices=[(1, '正常'), (2, '禁用')], default=1, help_text='状态：1-正常 2-禁用', verbose_name='状态：1-正常 2-禁用')),
                ('note', models.CharField(help_text='个人备注', max_length=255, null=True, verbose_name='个人备注')),
                ('sort', models.IntegerField(default=0, help_text='排序', verbose_name='排序')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'django_user',
            },
        ),
    ]