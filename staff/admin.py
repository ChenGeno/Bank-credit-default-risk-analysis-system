from django.contrib import admin
from .models import Staff  # 导入Staff模型

# Register your models here.
# 注册Staff到admin中
admin.site.register(Staff)
