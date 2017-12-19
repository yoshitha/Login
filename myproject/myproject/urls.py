"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from core import views as core_views
from django.views.generic.base import TemplateView

urlpatterns = [
	path('account_activation_sent/', core_views.account_activation_sent, name = 'account_activation_sent'),
	#url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', core_views.activate, name='activate'),
	path('activate/<uidb64>/<token>', core_views.activate, name = 'activate'),
	path('accounts/profile/', TemplateView.as_view(template_name='home.html'), name='home'),
	path('signup/', core_views.signup, name='signup'),
	path('login/', auth_views.login, {'template_name' : 'registration/login.html'}, name='login'),
	path('logout/', auth_views.logout, {'template_name' : 'registration/logged_out.html'}, name='logout'),

	path('admin/', admin.site.urls),
]
