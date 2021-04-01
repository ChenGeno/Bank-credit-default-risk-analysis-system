# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User

# 登录表单，继承了 forms.Form类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserRegisterForm(forms.ModelForm):
    # 复写User的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User  # 抽象User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试。")