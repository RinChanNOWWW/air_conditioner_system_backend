"""air_conditioner_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.views import RoomStatusView, RoomLogView, RoomCheckView
from apscheduler.schedulers.background import BackgroundScheduler
from backend.poll import poll, poll2
# from datetime import datetime

apis = [
    path('room_status/', RoomStatusView.as_view(), name='room_status'),
    path('room_log/', RoomLogView.as_view(), name='room_log'),
    path('room_check/', RoomCheckView.as_view(), name='room_check')
]
urlpatterns = [
    path(r'api/', include(apis))
    # path('admin/', admin.site.urls),
]

sched = BackgroundScheduler()

sched.add_job(poll2, 'interval', seconds=5)

sched.start()

