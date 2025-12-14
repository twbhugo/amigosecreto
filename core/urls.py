"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from core.views import addGuest, home, dashboard, logout, confirm_assistance, view_secret_friend, console, admin_console, save_family_group, assigments, save_gift_idea

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout, name='logout'),
    path('confirmacion/', confirm_assistance, name='confirm_assistance'),
    path('amigosecreto/', view_secret_friend, name='view_secret_friend'),
    path('console/', console, name='console'),
    path('console/admin/', admin_console, name='admin_console'),
    path('console/save_family_group/', save_family_group, name='save_family_group'),
    path('console/add_guest/', addGuest, name='addGuest'),
    path('assigments/', assigments, name='assigments'),
    path('save_gift_idea/', save_gift_idea, name='save_gift_idea'),
]
