from models import City, Transport
from rest_framework import filters


class CityFilter(filters.FilterSet):
    class Meta:
        model = City
        fields = ['place_id']


class TransportFilter(filters.FilterSet):
    class Meta:
        model = Transport
        fields = ['logistic_center', 'is_active']