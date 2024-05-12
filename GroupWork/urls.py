"""
URL configuration for GroupWork project.

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
from neo.views import system, zstp_show, select_attribute, simple_select_herb, simple_select_medicine, simple_select_prescr, cypher_change, welcome, admin_list, admin_role, smart_qa, smart_consult,bot_response
urlpatterns = [
    path('admin/', admin.site.urls),
    path('system/zstp_show.html', zstp_show),
    path('system/', system),
    path('system/welcome.html', welcome),
    path('system/select_attribute.html', select_attribute),
    path('system/simple_select_herb.html', simple_select_herb),
    path('system/simple_select_medicine.html', simple_select_medicine),
    path('system/simple_select_prescr.html', simple_select_prescr),
    path('system/cypher_change.html', cypher_change),
    path('system/admin-list.html',admin_list),
    path('system/admin-role.html',admin_role),
    path('system/smart_QA.html', smart_qa),
    path('system/smart_Consult.html', smart_consult),
    path('get', bot_response, name='bot_response'),
]
