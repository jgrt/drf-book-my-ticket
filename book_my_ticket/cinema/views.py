import logging

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError

from .models import (
    City, Brand, Cinema,
    Screen, Movies, SeatCategory, Showtime,
)
from .serializers import (
    CitySerializer, BrandSerializer, CinemaSerializer,
    ScreenSerializer, MovieSerializer, SeatCategorySerializer,
    MoviesWithCity, ShowtimeSerializer, CinemaWithMovies
)


def validate_date_range(payload):
    if 'start_date' not in payload:
        start = timezone.now()
    if 'end_date' not in payload:
        end = timezone.now() + timedelta(days=7)
    try:
        start = parse_datetime(payload['start_date'])
        end = parse_datetime(payload['end_date'])
        assert start and end, "cannot parse datetime"

    except Exception as e:
        logging.warning(e)
        raise ValidationError("Invalid Datetime format, Can not parse")

    if start < timezone.now():
        raise ValidationError("Can not visit past, Sorry!")

    if start > end:
        raise ValidationError("End must occur after Start")

    return start, end


class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = City.objects.all()
    serializer_class = CitySerializer


class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CinemaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class ScreenDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


class ScreenList(generics.ListCreateAPIView):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer


class MovieList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer


class SeatCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = SeatCategory.objects.all()
    serializer_class = SeatCategorySerializer


class SeatCategoryList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = SeatCategory.objects.all()
    serializer_class = SeatCategorySerializer


class ShowtimeList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer


class MoviesByCity(generics.GenericAPIView):
    serializer_class = MoviesWithCity

    def post(self, request):
        payload = request.data
        city = get_object_or_404(City, pk=payload["city"])
        start, end = validate_date_range(payload)
        movies_id = Showtime.objects.filter(screen__cinema__city=city, date_time__range=(start, end)).values_list('movie', flat=True)
        movies = Movies.objects.filter(id__in=movies_id)
        return Response(MovieSerializer(list(movies), many=True).data)


class CinemaByMovie(generics.GenericAPIView):
    serializer_class = CinemaWithMovies

    def post(self, request):
        payload = request.data
        start, end = validate_date_range(payload)
        movie = get_object_or_404(Movies, pk=payload["movie"])
        city = get_object_or_404(City, pk=payload["city"])
        showtimes = Showtime.objects.filter(movie=movie, screen__cinema__city=city, date_time__range=(start, end))
        print(showtimes)
        return Response('ok')



