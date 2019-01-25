
from management import models
from stark.service.stark import site

from management.views.userinfo import UserInfoHandler #用户的视图
from management.views.school import SchoolHandler   #学校的视图
from management.views.depart import DepartHandler   #部门的视图
from management.views.classes import ClassesHandler #班级的视图
from management.views.private_customer import PrivateCustomerHandler   #客户的视图，包含公户和私户
from management.views.public_customer import PublicCustomerHandler #班级的视图
from management.views.consult_record import ConsultRecordHandler
# 注册到stark组件中

site.register(models.UserInfo, UserInfoHandler)
site.register(models.Depart, DepartHandler)
site.register(models.School, SchoolHandler)
site.register(models.ClassList, ClassesHandler)

site.register(models.Customer, PublicCustomerHandler, 'pub') #公户
site.register(models.Customer, PrivateCustomerHandler, 'priv') # 私户
site.register(models.ConsultRecord,ConsultRecordHandler)

# 跟进记录
