from models import City
from rest_framework import filters


class CityFilter(filters.FilterSet):
    class Meta:
        model = City
        fields = ['name']