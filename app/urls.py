"""nols URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app import views
from django.urls import path


app_name = 'app'
urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('index/device_add/', views.dev_add, name='dev_add'),
    path('index/device_add/dev/', views.dev_add_dev, name='dev_add_dev'),
    path('index/device_add/del/', views.dev_add_del, name='dev_add_del'),
    path('index/policy/', views.policy, name='policy'),
    path('index/device_group/', views.dev_group, name='dev_group'),
    path('index/decode/', views.decode, name='decode'),
    path('index/ip_location/', views.ip_location, name='ip_location'),
    path('index/device_group/del/', views.dev_group_del, name='dev_group_del'),
    path('index/device_type/',views.device_type,name='dev_type'),
    path('index/device_mgt/',views.dev_mgt,name='dev_mgt'),
    path('index/device_mgt/del/',views.dev_mgt_del,name='dev_mgt_del'),
    path('index/device_type/del/',views.type_del,name='type_del'),
    path('logout/',views.login_out,name='logout'),
    path('index/policy_group_del/',views.policy_group_del,name='policy_group_del'),
    path('index/policy_group_edit/',views.policy_group_edit,name='policy_group_edit'),
    path('index/monitor/',views.monitor,name='monitor'),
    path('index/monitor/del/',views.monitor_del,name='monitor_del'),
    path('index/monitor/search/',views.monitor_search,name='monitor_search'),
    path('index/monitor/status/',views.monitor_status,name='monitor_status'),
    path('index/monitor/export/',views.monitor_export,name='monitor_export'),
    path('index/monitor/check_cf/',views.monitor_check_cf,name='monitor_check_cf'),
    path('index/wxfx/',views.wxfx,name='wxfx'),
    path('index/wxfx_del/',views.wxfx_del,name='wxfx_del'),
    path('index/wxfx/export/',views.wxfx_export,name='wxfx_export'),
    path('index/wxfx/status/',views.wxfx_status,name='wxfx_status'),
    path('index/wxfx/wxfx_search/', views.wxfx_search, name='wxfx_search'),
    path('index/log/fdjl/',views.fdjl,name='fdjl'),
    path('index/log/fdjl_export/',views.fdjl_export,name='fdjl_export'),
    path('index/log/fdjl_search/', views.fdjl_search, name='fdjl_search'),
    path('index/messges/',views.messges,name='messges'),
    path('index/js_code/',views.js_code,name='js_code'),
    path('index/js_code/view/',views.js_view,name='js_view'),
    path('index/js_code/del/',views.js_del,name='js_del'),
    path('index/test/',views.test_sad,name='test'),



]
