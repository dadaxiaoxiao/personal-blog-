from django import forms
from django.contrib.auth.models import User  #引用django 默认的用户模型
from .models import UserProfile,UserInfo

# 登录表单
class LoginForm(forms.Form):
    username= forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)

#注册表单
class RegistrationForm(forms.ModelForm):
    password = forms.CharField( label="Password", widget=forms.PasswordInput)
    password2 =forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    class Meta:   #声明本表单所引用的数据模型
        model = User
        fields =("username","email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']


#增加注册内容表单
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone","birth")

#个人信息表单
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school","company","profession","address","aboutme","photo")

#要修改django 默认的数据库中的 email
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)