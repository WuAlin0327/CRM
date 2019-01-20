from stark.service.stark import  BaseModelForm,StarkForm
from django import forms
from django.forms.utils import ValidationError
from management import models
from management.utils.md5 import gen_md5
class AddUserModelForm(BaseModelForm):
    """
        添加用户的ModelForm
    """
    r_password = forms.CharField(max_length=32,label='确认密码',widget=forms.PasswordInput())
    password = forms.CharField(max_length=32,label='密码',widget=forms.PasswordInput())

    class Meta:
        model = models.UserInfo
        fields = ['username','password','name','r_password','email','phone','gender','depart']
    def clean_r_password(self):
        password = self.cleaned_data['password']
        r_password = self.cleaned_data['r_password']
        if not password == r_password:
            raise ValidationError('两次密码输入不一致')
        return r_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data

class UpdateUserModelForm(BaseModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name','email','phone','gender','depart']

class ResetPasswordModelForm(StarkForm):
    password = forms.CharField(max_length=255,widget=forms.PasswordInput(),label='请输入密码')
    r_password = forms.CharField(max_length=255,widget=forms.PasswordInput(),label='请重新输入密码')

    def clean_r_password(self):
        password = self.cleaned_data['password']
        r_password = self.cleaned_data['r_password']
        if password != r_password:
            raise ValidationError('两次密码输入不一致，请重新输入')
        return r_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data