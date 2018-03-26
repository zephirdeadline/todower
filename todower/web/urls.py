"""supervisorstable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main/$', views.main, name='main'),
    url(r'^change/(?P<id_task>[0-9]+)/(?P<list_number>[0-9]+)/$', views.change, name='change'),
    url(r'^add_task/$', views.add_task, name='add_task'),
    url(r'^history/$', views.history, name='history'),
    url(r'^update_task/(?P<id_task>[0-9]+)$', views.update_task, name='update_task')
]
