import models
from rest_framework import serializers


class CitySerializer(serializers.ModelSerializer):
    logistic_centers = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        model = models.City
        fields = (
            'id', 'name', 'lat', 'lng', 'place_id', 'logistic_centers',
            'flying_altitude'
        )


class StyleURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StyleURL
        fields = (
            'id', 'name', 'earth_url', 'maps_url', 'scale')


class DefinedStyleSerializer(serializers.ModelSerializer):
    dp = StyleURLSerializer(many=False, read_only=True)
    lc = StyleURLSerializer(many=False, read_only=True)

    class Meta:
        model = models.DefinedStyle
        fields = (
            'id', 'name', 'dp', 'lc')


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transport
        fields = (
            'id', 'status', 'package', 'logistic_center', 'drone', 'step',
            'max_steps')


class PackageSerializer(serializers.ModelSerializer):
    transport = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Package
        fields = (
            'id', 'name', 'drop_point', 'transport', 'style_url')


class DroneSerializer(serializers.ModelSerializer):
    transports = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Drone
        fields = (
            'id', 'model', 'plate', 'status', 'battery_life',
            'logistic_center', 'style_url', 'transports')


class DropPointSerializer(serializers.ModelSerializer):
    packages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.DropPoint
        fields = (
            'id', 'name', 'description', 'lat', 'lng', 'alt',
            'logistic_center', 'packages')


class LogisticCenterSerializer(serializers.ModelSerializer):
    droppoints = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    drones = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.LogisticCenter
        fields = (
            'id', 'name', 'address', 'description', 'lat', 'lng',
            'alt', 'radius', 'defined_style', 'city', 'droppoints', 'drones')
