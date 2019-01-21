from django.db import models
from rbac.models import UserInfo as User


# Create your models here.

class School(models.Model):
    """
    校区表
    """
    title = models.CharField(verbose_name='校区名称', max_length=32)

    def __str__(self):
        return self.title


class Depart(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门名称', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(User):
    name = models.CharField(verbose_name='真名', max_length=16, default='miao')
    phone = models.IntegerField(verbose_name='电话号码')
    gen = (
        (1, '男'),
        (2, '女')
    )
    gender = models.IntegerField(verbose_name='性别', choices=gen, default=1)
    depart = models.ForeignKey(verbose_name='部门', to='Depart', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    课程表
    """
    name = models.CharField(max_length=32, verbose_name='课程名')

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """
    班级表
    """
    school = models.ForeignKey(verbose_name='校区', to='School', on_delete=models.CASCADE)
    course = models.ForeignKey(verbose_name='课程名称', to='Course', on_delete=models.CASCADE)
    semester = models.PositiveIntegerField(verbose_name='班级(期)')
    price = models.PositiveIntegerField(verbose_name='学费')
    start_date = models.DateField(verbose_name='开班日期')
    graduate_date = models.DateField(verbose_name='结业日期', null=True, blank=True)

    class_teacher = models.ForeignKey(verbose_name='班主任', to='UserInfo', on_delete=models.CASCADE,
                                      related_name='classes', limit_choices_to={'depart__title': '教质部'})
    # limit_choices_to默认在filter中加入这个
    tech_teacher = models.ManyToManyField(verbose_name='任课老师', to='UserInfo', blank=True,
                                          limit_choices_to={'depart__title': '教学部'})
    memo = models.TextField(verbose_name='说明', null=True, blank=True)

    def __str__(self):
        return '%s%s期' % (self.course.name, self.semester)


class Customer(models.Model):
    """
    客户表
    """
    qq = models.CharField(verbose_name='联系方式', max_length=64, unique=True, help_text='QQ号/微信/手机号')
    name = models.CharField(verbose_name='姓名', max_length=16)
    status_choices = [
        (1, '已报名'),
        (2, '未报名')
    ]
    status = models.IntegerField(
        verbose_name='状态',
        choices=status_choices,
        default=2,
        help_text='客户是否已报名'
    )
    gender_choice = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice, default=1)
    source_choices = [
        (1, 'QQ群'),
        (2, '内部转介绍'),
        (3, '官方网站'),
        (4, '百度推广'),
        (5, '360推广'),
        (6, '搜狗推广'),
        (7, '腾讯课堂'),
        (8, '广点通'),
        (9, '高校宣讲'),
        (10, '据道代理'),
        (11, '51cto'),
        (12, '智慧推'),
        (13, 'DSP'),
        (14, 'SEO'),
        (15, '其他'),
        (16, '网盟'),
    ]
    source = models.SmallIntegerField(verbose_name='客户来源', choices=source_choices, default=15)
    referral_from = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name='转介绍自学员',
        help_text='若此客户是转介绍自内部学员，请在此处选择内部学员姓名',
        related_name='internal_referral',
        on_delete=models.CASCADE
    )
    consultant = models.ForeignKey(verbose_name='课程顾问', to='UserInfo', related_name='consultant', null=True, blank=True,
                                   on_delete=models.CASCADE)
    course = models.ManyToManyField(verbose_name='咨询课程', to='Course')
    education_choices = (
        (1, '重点大学'),
        (2, '普通本科'),
        (3, '独立院校'),
        (4, '民办本科'),
        (5, '大专'),
        (6, '民办专科'),
        (7, '高中'),
        (8, '其他'),
    )
    education = models.IntegerField(verbose_name='学历', choices=education_choices, blank=True, null=True)
    graduation_shcool = models.CharField(verbose_name='毕业学校', max_length=64, blank=True, null=True)
    major = models.CharField(verbose_name='专业', max_length=64, blank=True, null=True)
    experence_choices = (
        (1, '在校生'),
        (2, '应届毕业'),
        (3, '半年以内'),
        (4, '半年至一年'),
        (5, '一年至三年'),
        (6, '三年至五年'),
        (7, '五年以上'),
    )
    experence = models.IntegerField(verbose_name='工作经验', null=True, blank=True, choices=experence_choices)
    work_status_choices = (
        (1, '在职'),
        (2, '无业'),
    )
    work_status = models.IntegerField(verbose_name='职业状态', default=1, blank=True)
    company = models.CharField(verbose_name='目前就职公司', max_length=64, blank=True, null=True)
    salary = models.CharField(verbose_name='当前薪资', max_length=64, blank=True, null=True)
    date = models.DateField(verbose_name='咨询时间', auto_now_add=True)
    last_consult_date = models.DateField(verbose_name='最后跟进日期', auto_now_add=True)

    def __str__(self):
        return "姓名：%s,联系方式:%s" % (self.name, self.qq)
