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
from dlp import models, views

# router = routers.DefaultRouter()
# router.register(r'drone', views.DroneViewSet.as_view())
# router.register(r'droppoints', views.DropPointViewSet, 'droppoints')
# router.register(r'meteostations', views.MeteoStationViewSet, 'meteostations')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.base),
    url(r'^crud/logisticCenter/?$', views.LogisticCenter.as_view(),
        name='logistic_center_view'),
    url(r'^crud/drone/?$', views.Drone.as_view(),
        name='drone_view'),
    url(r'^crud/dropPoint/?$', views.Droppoint.as_view(),
        name='drop_point_view'),
    url(r'^crud/city/?$', views.City.as_view(),
        name='city_view'),
    url(r'^crud/package/?$', views.Package.as_view(),
        name='package_view'),
    url(r'^crud/transport/?$', views.Transport.as_view(),
        name='transport_view'),
    # url(r'^api/', include(router.urls)),
    # url(r'^api-auth/',
    #     include('rest_framework.urls', namespace='rest_framework')),
]
