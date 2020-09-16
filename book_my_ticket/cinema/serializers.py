from rest_framework import serializers
from .models import City, Brand, Cinema, Screen, Movies, SeatCategory, Seat, MovieInCity


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class CinemaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ['id', 'name', 'address', 'brand', 'city']


class ScreenSerializers(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ['id', 'name', 'brand', 'city', 'cinema']


class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['id', 'name', 'runtime']


class SeatCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = SeatCategory
        fields = ['id', 'name', 'brand']


class SeatSerializers(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'cinema', 'screen', 'category', 'seats']


class MovieInCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieInCity
        fields = ['id', 'movie', 'city', 'is_available']

