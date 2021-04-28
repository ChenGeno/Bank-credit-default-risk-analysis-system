# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from .models import Profile

# 登录表单，继承了 forms.Form类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
# 注册表单
class UserRegisterForm(forms.ModelForm):
    # 复写User的密码
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User  # 抽象User
        fields = ('username', 'email', 'first_name', 'last_name')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试。")

# 引入 Profile 模型(与User一对一的延伸字段)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('member_id', 'avatar')
