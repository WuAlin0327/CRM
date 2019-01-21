from management import handler
from management import models
from stark.service.stark import site


# 注册到stark组件中
site.register(models.Course,handler.CourseHandler)
site.register(models.UserInfo, handler.UserInfoHandler)
site.register(models.Depart, handler.DepartHandler)
site.register(models.School, handler.SchoolHandler)
site.register(models.ClassList,handler.ClassesHandler)

