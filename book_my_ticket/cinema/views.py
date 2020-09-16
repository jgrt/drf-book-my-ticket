from django.shortcuts import render
from .models import City, Brand, Cinema, Screen, Movies, SeatCategory, Seat, MovieInCity
from .serializers import CitySerializers, BrandSerializers, CinemaSerializers, ScreenSerializers, \
    MovieSerializers, SeatCategorySerializers, SeatSerializers, MovieInCitySerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser


class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = City.objects.all()
    serializer_class = CitySerializers


class CityList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = City.objects.all()
    serializer_class = CitySerializers


class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers


class BrandList(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers


class CinemaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializers


class CinemaList(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializers


class ScreenDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializers


class ScreenList(generics.ListCreateAPIView):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializers


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializers


class MovieList(generics.ListCreateAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializers


class SeatCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SeatCategory.objects.all()
    serializer_class = SeatCategorySerializers


class SeatCategoryList(generics.ListCreateAPIView):
    queryset = SeatCategory.objects.all()
    serializer_class = SeatCategorySerializers


class SeatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializers


class SeatList(generics.ListCreateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializers


class MovieInCityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieInCity.objects.all()
    serializer_class = MovieInCitySerializer


class MovieInCityList(generics.ListCreateAPIView):
    queryset = MovieInCity.objects.all()
    serializer_class = MovieInCitySerializer
