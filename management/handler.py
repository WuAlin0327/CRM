"""
    Stark组件需要用的所有Handler都在这里
    相当于views
"""

from stark.service.stark import site, StarkHandler, Option
from . import model_form
from django.shortcuts import render, redirect, HttpResponse
from management import models
from django.utils.safestring import mark_safe
from django.conf.urls import url

class SchoolHandler(StarkHandler):
    list_display = [
        'id',
        'title',
    ]
    has_add_btn = True


class DepartHandler(StarkHandler):
    list_display = [
        'id',
        'title',
    ]

class UserInfoHandler(StarkHandler):
    @property
    def get_reset_url_name(self):
        return self.get_url_name('reset')

    def reset_password(self, request, pk, *args, **kwargs):
        """
        重置密码
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        userinfo_obj = models.UserInfo.objects.filter(pk=pk).first()
        if not userinfo_obj:
            return HttpResponse('该用户不存在')
        if request.method == 'GET':
            form = model_form.ResetPasswordModelForm()
            return render(request, 'stark/change.html', {'form': form})
        form = model_form.ResetPasswordModelForm(request.POST)
        if form.is_valid():
            userinfo_obj.password = form.cleaned_data['password']
            userinfo_obj.save()
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def extra_urls(self):
        """
         增加自定义的url
        :return:
        """
        patterns = [
            url(r'^reset/pwd/(?P<pk>\d+)', self.wrapper(self.reset_password), name=self.get_reset_url_name)
        ]
        return patterns

    def display_reset_password(self, obj, is_head=None):
        if is_head:
            return '重置密码'
        url = self.reverse_name_url(name=self.get_reset_url_name, pk=obj.pk)
        return mark_safe('<a href="%s">重置密码</a>' % url)

    list_display = [
        'username',
        'name',
        'email',
        'phone',
        StarkHandler.get_choice_text('性别', 'gender'),
        'depart',
        display_reset_password

    ]
    search_list = ['username__contains', 'name__contains', 'email__contains']
    search_group = [
        Option('gender'),
        Option('depart', is_multi=True)
    ]

    def get_model_form_class(self, is_add=None):
        if is_add:
            return model_form.AddUserModelForm
        else:
            return model_form.UpdateUserModelForm


class CourseHandler(StarkHandler):
    list_display = [
        'name',
    ]


class ClassesHandler(StarkHandler):
    def display_semester(self,obj=None,is_head=None):
        if is_head:
            return '班级'
        return obj

    list_display = [
        'school',
        display_semester,
        'price',
        StarkHandler.get_datetime_text('开班日期','start_date'),
        'graduate_date',
        'class_teacher',
        StarkHandler.get_m2m_text('任课老师','tech_teacher'),
        'memo',
    ]
    model_form_class = model_form.ClassModelForm
    search_group = (
        Option('school'),
        Option('course'),
        Option('class_teacher'),
    )


    def change_view(self, request, pk, *args, **kwargs):
        """
        更改页面
        :param request:
        :return:
        """
        obj = self.model_class.objects.filter(id=pk)
        if not obj.first():
            return HttpResponse('要更改的数据不存在，请重新选择')
        form_class = self.get_model_form_class(is_add=False)
        if request.method == 'GET':
            form = form_class(instance=obj.first())
            return render(request, 'stark/change.html', {'form': form})
        form = form_class(request.POST)
        if form.is_valid():
            teacher = form.cleaned_data.pop('tech_teacher')
            obj.first().tech_teacher.set(teacher)
            obj.update(**form.cleaned_data)
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})


class CustomerHandler(StarkHandler):
    pass


