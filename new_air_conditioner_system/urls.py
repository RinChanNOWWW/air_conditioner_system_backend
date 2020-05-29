"""new_air_conditioner_system URL Configuration

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
from backend import views
from apscheduler.schedulers.background import BackgroundScheduler
from backend import controller

admin_apis = [
    path('setup/', views.SetUp.as_view(), name='setup'),
    path('monitor/', views.Monitor.as_view(), name='monitor')
]

user_apis = [
    path('checkin/', views.CheckIn.as_view(), name='checkin'),
    path('setmode/', views.SetMode.as_view(), name='setmode'),
    path('heartbeat/', views.HeartBeat.as_view(), name='heartbeat')
]

front_apis = [
    path('checkout/', views.CheckOut.as_view(), name='checkout')
]

manager_apis = [
    path('report/', views.Report.as_view(), name='report')
]

apis = [
    path('admin/', include(admin_apis)),
    path('user/', include(user_apis)),
    path('front/', include(front_apis)),
    path('manager/', include(manager_apis)),
]



urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include(apis))
]

background_scheduler = BackgroundScheduler()
background_scheduler.add_job(
    controller.poll,
    'interval',
    seconds=controller.interval
)
background_scheduler.start()

