"""
URL configuration for project project.

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
from user import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',user_views.home,name='home'),
    path('about',user_views.about,name='about'),
    path('contact',user_views.contact,name='contact'),
    path('user-login',user_views.user_login,name='user_login'),
    path('user-gpi-register',user_views.gpi_register,name='gpi_register'),
    path('user-gpi-login',user_views.gpi_login,name='gpi_login'),
    path('user-gpi-update',user_views.gpi_update,name='gpi_update'),
    path('otp-verification/<int:o_id>',user_views._send_otpp,name='send_otp'),
    path('otp-validation/<int:gen_otp>/<int:otp>/<int:o_id>',user_views.otp_validation,name='otp_validation'),
    path('user-register',user_views.user_register,name='user_register'),
    path('log-out',user_views.log_out,name='log_out'),
    path('forget-password',user_views.forget_password,name='forget_password'),
    path('reset-password/<str:id>/',user_views.reset_password,name="reset_password"),
    path('change-password',user_views.change_password,name="change_password"),
    path('base',user_views.base,name='base'),
    path('myprofile',user_views.myprofile,name='myprofile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
