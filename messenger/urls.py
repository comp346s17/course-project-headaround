from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'messenger/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^accounts/profile/', views.home, name='home'),
    url(r'^message/$', views.message, name='message'),
    url(r'^guess/$', views.guess, name='guess'),
    url(r'^messageDetail/$', views.messageDetail, name='messageDetail'),
]

