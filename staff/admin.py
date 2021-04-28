from django.contrib import admin
from .models import Staff  # 导入Staff模型
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.
# 注册Staff到admin中
admin.site.register(Staff)


# 定义一个行内 admin（用于在admin中将User、Profile合并为一张完整的表格）
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'


# 将 Profile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

