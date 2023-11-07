from django.contrib import admin

# Register your models here.
from application.level.models import Level

# 把models创建的表，添加到admin后台
admin.site.register(Level)
