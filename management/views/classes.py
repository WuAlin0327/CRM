from stark.service.stark import site, StarkHandler, Option
from management import model_form
from django.shortcuts import render, redirect, HttpResponse


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