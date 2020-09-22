from django.urls import path, re_path
from .views import (
    CityList,
    CityDetail,
    BrandList,
    BrandDetail,
    CinemaList,
    CinemaDetail,
    ScreenList,
    ScreenDetail,
    MovieList,
    MovieDetail,
    SeatCategoryList,
    SeatCategoryDetail,
    MoviesByCity,
    ShowtimeList,
    CinemaByMovie,
    ScreenCapacityList,
    SeatAvailability,
    SeatBooking,
)


urlpatterns = [
    path("city/", CityList.as_view()),
    path("city/<int:pk>/", CityDetail.as_view()),
    path("brand/", BrandList.as_view()),
    path("brand/<int:pk>/", BrandDetail.as_view()),
    path("cinema/", CinemaList.as_view()),
    path("cinema/<int:pk>/", CinemaDetail.as_view()),
    path("screen/", ScreenList.as_view()),
    path("screen/<int:pk>/", ScreenDetail.as_view()),
    path("screen_capacity", ScreenCapacityList.as_view()),
    path("movie/", MovieList.as_view()),
    path("movie/<int:pk>/", MovieDetail.as_view()),
    path("seat_category/", SeatCategoryList.as_view()),
    path("seat_category/<int:pk>/", SeatCategoryDetail.as_view()),
    path("showtime/", ShowtimeList.as_view()),
    path("movies_by_city/", MoviesByCity.as_view()),
    path("cinema_by_movie/", CinemaByMovie.as_view()),
    re_path(
        r"^check_seat_availability/(?P<showtime_id>[0-9]+)/$",
        SeatAvailability.as_view(),
    ),
    path("book_seat/", SeatBooking.as_view()),
]
