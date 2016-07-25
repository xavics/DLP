"""DLP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from dlp import models, views


router = DefaultRouter()
router.register(r'cities', views.CityViewSet)
router.register(r'styleurls', views.StyleURLViewSet)
router.register(r'definedstyles', views.DefinedStyleViewSet)
router.register(r'droppoints', views.DropPointViewSet)
router.register(r'drones', views.DroneViewSet)
router.register(r'packages', views.PackageViewSet)
router.register(r'transports', views.TransportViewSet)
router.register(r'logisticcenters', views.LogisticCenterViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.base),
    url(r'^receive_position$', views.receive_position),
    url(r'^update_logistic_centers', views.update_logistic_centers),
    url(r'^update_droppoints', views.update_droppoints),
    url(r'^api/', include(router.urls)),
    url(r'^refreshweather/$', views.refresh_weather),
    # url(r'^api-auth/',
    #     include('rest_framework.urls', namespace='rest_framework')),
]
