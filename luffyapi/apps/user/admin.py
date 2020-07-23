from django.contrib import admin


# Register your models here.
# class GlobalSettings(object):
#
#     site_title = "路飞学城"  # 设置站点标题
#     site_footer = "路飞学城有限公司"  # 设置站点的页脚
#     # menu_style = "accordion"  # 设置菜单折叠
#
#
# admin.site.register(views.CommAdminView, GlobalSettings)

from . import models
admin.site.register(models.User)