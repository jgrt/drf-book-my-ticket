from django.urls import path, include, re_path
from .views import ListAllAvailableMovies

urlpatterns = [
    re_path(r'^movie_by_city/(?P<city_id>[-\w]+)/$', ListAllAvailableMovies.as_view())
]
