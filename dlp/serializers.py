import models
from rest_framework import serializers


# class DropPointSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.DropPoint
#         fields = (
#             'id', 'name', 'description', 'latitude', 'longitude', 'altitude',
#             'is_available')
#
#
# class LogisticCenterSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.LogisticCenter
#         fields = (
#             'id', 'address', 'description', 'latitude', 'longitude',
#             'altitude', 'radius', 'is_available')
#
#
# class DroneSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.LogisticCenter
#         fields = (
#             'id', 'model', 'plate', 'latitude', 'longitude', 'is_available')
#
#
# class PackageSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.LogisticCenter
#         fields = (
#             'id', 'name')
