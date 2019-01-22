"""
    Stark组件需要用的所有Handler都在这里
    相当于views
"""

from stark.service.stark import site, StarkHandler, Option
from management import model_form
from django.shortcuts import render, redirect, HttpResponse
from management import models
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.db.models import Avg, Count
from django.db import transaction


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
    def display_semester(self, obj=None, is_head=None):
        if is_head:
            return '班级'
        return obj

    list_display = [
        'school',
        display_semester,
        'price',
        StarkHandler.get_datetime_text('开班日期', 'start_date'),
        'graduate_date',
        'class_teacher',
        StarkHandler.get_m2m_text('任课老师', 'tech_teacher'),
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





class PublicCustomerHandler(StarkHandler):
    """
    公户：
        与私户的差别：公户没有课程顾问
    """
    def display_record(self, obj=None, is_head=None):
        if is_head:
            return '查看跟进记录'
        url = self.reverse_name_url(self.get_record_url_name, pk=obj.pk)

        return mark_safe('<a href="%s">查看跟进<a/>' % url)
    @property
    def get_record_url_name(self):
        """
        跟进记录url
        :return:
        """
        return self.get_url_name('record')
    def extra_urls(self):
        """
         增加自定义的url
        :return:
        """
        patterns = [
            url(r'^record/(?P<pk>\d+)', self.wrapper(self.record_view), name=self.get_record_url_name)
        ]
        return patterns
    def record_view(self, request, pk):

        record_list = models.ConsultRecord.objects.filter(consultant_id=pk)
        f = open('/Users/wualin/Documents/pychon/CRM/management/三国演义.txt', 'r')

        return render(request, 'record.html', {'data_list': record_list, 'file': f})

    model_form_class = model_form.CustomerModelForm
    list_display = [
        StarkHandler.display_checkbox,
        'name',
        'qq',
        StarkHandler.get_choice_text('状态', 'status'),
        StarkHandler.get_choice_text('性别', 'gender'),
        StarkHandler.get_choice_text('客户来源', 'source'),
        'referral_from',
        'consultant',
        StarkHandler.get_m2m_text('咨询课程', 'course'),
        StarkHandler.get_choice_text('学历', 'education'),
        'graduation_shcool',
        'major',
        StarkHandler.get_choice_text('工作经验', 'experence'),
        StarkHandler.get_datetime_text('咨询时间', 'date'),
        display_record,
    ]

    def multi_apply(self, request, *args, **kwargs):
        """
            批量操作
        :param request:
        :return:
        """
        # 用户id
        user_id = request.session['user'].get('id')
        depart = request.session['user'].get('depart')
        if depart != '销售部':return HttpResponse('只有销售部的员工才可以将客户添加到私户')
        if not user_id:
            return redirect('/login/')

        # 客户ID
        pk_list = request.POST.getlist('pk')
        if not pk_list:
            return HttpResponse('请选择需要申请添加到私户的客户')
        # 将选中的客户更新到我的私户中：更新consultant字段
        count = models.Customer.objects.filter(consultant_id=user_id, status=2).count()
        if (count + len(pk_list)) < 150: # 对于私护个人的限制
            # 在Django中给数据库加锁,保证数据安全
            flag = False
            with transaction.atomic():# 数据库
                orgin_queryset = models.Customer.objects.filter(pk__in=pk_list, status=2, consultant__isnull=True).select_for_update()
                if len(orgin_queryset) ==len(pk_list):
                    models.Customer.objects.filter(pk__in=pk_list, status=2, consultant__isnull=True).update(
                        consultant_id=user_id)
                    flag = True
            if not flag:
                return HttpResponse('手速太慢了，选中的客户已被其他人申请，请重新选择')
        else:
            return HttpResponse('你未转化的客户超过了150人，私户中已有%s未转化的客户' % count)

    multi_apply.text = '批量申请到私户'
    action_list = [
        multi_apply
    ]

    def change_view(self, request, pk, *args, **kwargs):

        obj = self.model_class.objects.filter(id=pk)
        if not obj.first():
            return HttpResponse('要更改的数据不存在，请重新选择')
        form_class = self.get_model_form_class(is_add=False)
        if request.method == 'GET':
            form = form_class(instance=obj.first())
            return render(request, 'stark/change.html', {'form': form})
        form = form_class(request.POST)
        if form.is_valid():
            course = form.cleaned_data.pop('course')
            obj.first().course.set(course)
            obj.update(**form.cleaned_data)
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def get_queryset(self, request, *args, **kwargs):
        # 页面查询时返回课程顾问为空的
        return self.model_class.objects.filter(consultant__isnull=True,status=2)


class PrivateCustomerHandler(PublicCustomerHandler):
    """
    私户
    """
    model_form_class = model_form.CustomerModelForm
    list_display = [
        'name',
        'qq',
        StarkHandler.get_choice_text('状态', 'status'),
        StarkHandler.get_choice_text('性别', 'gender'),
        StarkHandler.get_choice_text('客户来源', 'source'),
        'referral_from',
        'consultant',
        StarkHandler.get_m2m_text('咨询课程', 'course'),
        StarkHandler.get_choice_text('学历', 'education'),
        'graduation_shcool',
        'major',
        StarkHandler.get_choice_text('工作经验', 'experence'),
        StarkHandler.get_datetime_text('咨询时间', 'date'),
        PublicCustomerHandler.display_record
    ]
    action_list = []

    def get_queryset(self, request, *args, **kwargs):
        return self.model_class.objects.filter(consultant__isnull=False)
