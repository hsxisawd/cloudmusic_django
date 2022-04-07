"""cloudmusic_django URL Configuration

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
from django.contrib import admin
from django.urls import path

import cloudm.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",cloudm.views.index),
    path('get_hot_type/',cloudm.views.get_hot_type,name="get_hot_type"),
    path('get_hot_playlist/',cloudm.views.get_hot_playlist,name="get_hot_playlist"),
    path('get_month_data/',cloudm.views.get_month_data,name="get_month_data"),
    path('get_day_data/',cloudm.views.get_day_data,name="get_day_data"),
    path('get_track_data/',cloudm.views.get_track_data,name="get_track_data"),
    path('get_type_data/',cloudm.views.get_type_data,name="get_type_data"),
    path('get_map_data/',cloudm.views.get_map_data,name="get_map_data"),
]
