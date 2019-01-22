from management.views import handler
from management import models
from stark.service.stark import site


# 注册到stark组件中
site.register(models.Course, handler.CourseHandler)
site.register(models.UserInfo, handler.UserInfoHandler)
site.register(models.Depart, handler.DepartHandler)
site.register(models.School, handler.SchoolHandler)
site.register(models.ClassList, handler.ClassesHandler)

site.register(models.Customer, handler.PublicCustomerHandler, 'pub') #公户
site.register(models.Customer, handler.PrivateCustomerHandler, 'priv') # 私户

# 跟进记录
