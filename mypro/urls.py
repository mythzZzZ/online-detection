"""
URL configuration for mypro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views,pretty
from app01.vviews import  admin,account,task,order,chart,upload,city,obj_dec
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    # path("admin/", admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),


    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    path("depart/<int:nid>/edit/",views.depart_edit),
    path("user/list/",views.user_list),
    path("user/add/",views.user_add),
    path("user/model/form/add/",views.user_model_form_add),
    path("user/<int:nid>/edit/",views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),
    path('pretty/list/',pretty.pretty_list),
    path('pretty/add/',pretty.pretty_add),
    path("pretty/<int:nid>/edit/",pretty.pretty_edit),

    path('pretty/<int:nid>/delete/', pretty.user_delete),

    path('admin/list/',admin.admin_list),
    path('admin/add/',admin.admin_add),
    path('admin/<int:nid>/edit/',admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    path('task/list/',task.task_list),
    path('task/ajax/',task.task_ajax),
    path('task/add/',task.task_add),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),
    path('chart/highcharts/', chart.highcharts),
    # 上传文件
    path('upload/list/', upload.upload_list),
    path('upload/modal/form/', upload.upload_modal_form),

    # 城市列表
    path('city/list/', city.city_list),
    path('city/add/', city.city_add),

    path('obj/modal/form/', obj_dec.obj_upload_modal_form),
    path('obj/list/', obj_dec.obj_list),

]
