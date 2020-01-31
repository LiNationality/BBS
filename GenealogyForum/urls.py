"""GenealogyForum URL Configuration

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
from django.conf.urls import url,include
from web_app import views
urlpatterns = [
    url(r'^my_admin/',include('my_admin.urls')),
    url(r'^test/',include('test_app.urls')),
    path('admin/', admin.site.urls),
    url(r'^login/$',views.login,name='login'),
    url(r'^check_code.html$', views.check_code,name='check_code'),
    url('^index/$',views.index,name='index'),
    url('test/$',views.test,name='test'),
    url('^user_info/$',views.user_info,name='user_info'),
    url(r'^pwd_edit/$',views.pwd_edit,name='pwd_edit'),
    url(r'my_art/$',views.my_art,name='my_art'),
    #url(r'logout/$',views.my_logout,'logout'),
    url(r'home/',views.home,name='home'),
    url(r'all_top/',views.all_top,name='all_top'),
    url(r'^publish/',views.publish,name='publish'),
    url(r'^single/(?P<tid>\d+)/', views.single),
    url(r'^all_top-(?P<kid>\d+)-(?P<reply_limit>\d+)-(?P<time_limit>\d+)', views.all_top),  # 按条件搜索帖子
]
