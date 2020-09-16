from cinema.models import City, Brand, Cinema, Screen, Movies, SeatCategory, Seat, MovieInCity
from cinema.serializers import CitySerializers, BrandSerializers, CinemaSerializers, ScreenSerializers, \
    MovieSerializers, SeatCategorySerializers, SeatSerializers, MovieInCitySerializer
from rest_framework import generics


class ListAllAvailableMovies(generics.ListAPIView):
    serializer_class = MovieSerializers

    def get_queryset(self):
        queryset = MovieInCity.objects.filter(is_available=True)
        lookup_url_kwarg = 'city_id'
        if lookup_url_kwarg is not None:
            city_id = self.kwargs[lookup_url_kwarg]
            movies_ids = queryset.filter(city=city_id).values_list('movie', flat=True)
            movies = Movies.objects.filter(pk__in=movies_ids)
        return movies




