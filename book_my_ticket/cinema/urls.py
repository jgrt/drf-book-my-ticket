from django.urls import path
from .views import CityList, CityDetail, \
        BrandList, BrandDetail, \
        CinemaList, CinemaDetail, \
        ScreenList, ScreenDetail, \
        MovieList, MovieDetail, \
        SeatCategoryList, SeatCategoryDetail, \
        SeatList, SeatDetail, \
        MovieInCityList, MovieInCityDetail


urlpatterns = [
    path('city/', CityList.as_view()),
    path('city/<int:pk>/', CityDetail.as_view()),

    path('brand/', BrandList.as_view()),
    path('brand/<int:pk>/', BrandDetail.as_view()),

    path('cinema/', CinemaList.as_view()),
    path('cinema/<int:pk>/', CinemaDetail.as_view()),

    path('screen/', ScreenList.as_view()),
    path('screen/<int:pk>/', ScreenDetail.as_view()),

    path('movie/', MovieList.as_view()),
    path('movie/<int:pk>/', MovieDetail.as_view()),

    path('seat_category/', SeatCategoryList.as_view()),
    path('seat_category/<int:pk>/', SeatCategoryDetail.as_view()),

    path('seat/', SeatList.as_view()),
    path('seat/<int:pk>/', SeatDetail.as_view()),

    path('movie_in_city/', MovieInCityList.as_view()),
    path('movie_in_city/<int:pk>/', MovieInCityDetail.as_view()),

]