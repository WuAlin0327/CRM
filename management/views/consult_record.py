from stark.service.stark import StarkHandler
from django.conf.urls import url
from django.urls import reverse
from django import forms
from management.models import ConsultRecord
from management.model_form import RecoreModelForm
from django.shortcuts import render,redirect,HttpResponse


class ConsultRecordHandler(StarkHandler):
    customer_id = None
    change_list_template = 'consult_record.html'
    list_display = [
        'customer',
        'consultant',
        'date',
        'note'
    ]
    model_form_class = RecoreModelForm
    def get_urls(self):
        """
        对于一张表，默认定义了增删改查四个视图函数
            如果需要减少url或者重写url可以对该方法重写
        :return:
        """
        patterns = [
            url(r'^list/(?P<customer_id>\d+)/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
            url(r'^add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            url(r'^change/(?P<customer_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view), name=self.get_change_url_name),
            url(r'^delete/(?P<customer_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        customer_id = kwargs['customer_id']
        current_user_id = request.session['user'].get('id')
        return self.model_class.objects.filter(customer_id=customer_id,customer__consultant_id=current_user_id)

    def save(self,form,request,*args,**kwargs):
        customer_id = kwargs['customer_id']
        form.instance.customer_id = customer_id
        form.instance.consultant_id = request.session['user'].get('id')
        form.save()



