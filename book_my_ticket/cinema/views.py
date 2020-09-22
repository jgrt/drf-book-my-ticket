import logging
from django.db.models import Sum
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import timedelta
from rest_framework.exceptions import ValidationError
from auth_app.models import CustomUser
from .models import (
    City,
    Brand,
    Cinema,
    Screen,
    Movies,
    SeatCategory,
    Showtime,
    ScreenCapacity,
    Reservation,
    Booking,
)
from .serializers import (
    CitySerializer,
    BrandSerializer,
    CinemaSerializer,
    ScreenSerializer,
    MovieSerializer,
    SeatCategorySerializer,
    MoviesByCitySerialazer,
    ShowtimeSerializer,
    CinemaByMovieSerializer,
    ScreenCapacitySerializer,
    CinemaWithScreensOnly,
    ReservationSerializer,
    SeatBookingSerializer,
)


def validate_date_range(payload):
    if "start_date" not in payload:
        start = timezone.now()
    if "end_date" not in payload:
        end = timezone.now() + timedelta(days=7)
    try:
        start = parse_datetime(payload["start_date"])
        end = parse_datetime(payload["end_date"])
        assert start and end, "cannot parse datetime"

    except Exception as e:
        logging.warning(e)
        raise ValidationError("Invalid Datetime format, Can not parse")

    if start < timezone.now() - timedelta(hours=2):
        raise ValidationError("Can not visit past, Sorry!")

    if start > end:
        raise ValidationError("End must occur after Start")

    return start, end


def check_availability(showtime, seat_category=None):
    if not seat_category:
        seat_categories = (
            ScreenCapacity.objects.order_by("seat_category")
            .values_list("seat_category", flat=True)
            .distinct("seat_category")
        )
    else:
        seat_categories = [seat_category]
    resp = list()
    screen_capacity = (
        ScreenCapacity.objects.filter(
            screen=showtime.screen, seat_category__in=seat_categories
        )
        .values("seat_category")
        .annotate(no_of_seats=Sum("no_of_seats"))
    )
    for cap in screen_capacity:
        reserved = (
            Reservation.objects.filter(
                showtime=showtime.pk,
                seat_category=cap["seat_category"],
                showtime__status="CF",
            )
            .values("seat_category")
            .annotate(booked_seat=Sum("seats"))
        )
        if reserved.exists():
            available_seats = (
                cap["no_of_seats"] - reserved.values("booked_seat")[0]["booked_seat"]
            )
        else:
            available_seats = cap["no_of_seats"]
        if not available_seats < 1:
            _resp = dict(
                seat_category=cap["seat_category"], available_seats=available_seats
            )
            resp.append(_resp)
    return resp


class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get: return a city instance by id(pk).
    put: update city instance.
    delete: delete city instance.
    """

    permission_classes = [IsAdminUser]
    serializer_class = CitySerializer
    queryset = City.objects.all()


class CityList(generics.ListCreateAPIView):
    """
    get: List all the cities.
    post: Create a new city.
    """

    permission_classes = [IsAdminUser]
    queryset = City.objects.all()
    serializer_class = CitySerializer


class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get: return a brand instance by id(pk).
    put: update brand instance.
    delete: delete brand instance.
    """

    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandList(generics.ListCreateAPIView):
    """
    get: List all the brands.
    post: Create a new brand.
    """

    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CinemaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get: return a cinema instance by id(pk).
    put: update cinema instance.
    delete: delete cinema instance.
    """

    permission_classes = [IsAdminUser]
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaList(generics.ListCreateAPIView):
    """
    get: List all the cinemas in the system.
    post: Create a new cinema.
    """

    permission_classes = [IsAdminUser]
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class ScreenDetail(generics.RetrieveUpdateDestroyAPIView):
    """
   get: return a screen/auditorium instance by id(pk).
   put: update screen instance.
   delete: delete screen instance.
   """

    permission_classes = [IsAdminUser]
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


class ScreenList(generics.ListCreateAPIView):
    """
    get: List all the screens.
    post: Create a new screen.
    """

    permission_classes = [IsAdminUser]
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


class ScreenCapacityList(generics.ListCreateAPIView):
    """
    get: List all the screen capacity in terms of seats with their category ex-Platinum, Gold, Exclusive etc.
    post: Add a new screen capacity to screen along seat category.
    """

    permission_classes = [IsAdminUser]
    queryset = ScreenCapacity.objects.all()
    serializer_class = ScreenCapacitySerializer


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    """
   get: return a movie instance by id(pk).
   put: update movie instance.
   delete: delete movie instance.
   """

    permission_classes = [IsAdminUser]
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer


class MovieList(generics.ListCreateAPIView):
    """
    get: List all the movies in the system.
    post: Add a new movie.
    """

    permission_classes = [IsAdminUser]
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer


class SeatCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
   get: return a seat category instance by id(pk).
   put: update seat category instance.
   delete: delete seat category instance.
   """

    permission_classes = [IsAdminUser]
    queryset = SeatCategory.objects.all()
    serializer_class = SeatCategorySerializer


class SeatCategoryList(generics.ListCreateAPIView):
    """
    get: List all the seat categories in the system.
    post: Add a new seat categories.
    """

    permission_classes = [IsAdminUser]
    queryset = SeatCategory.objects.all()
    serializer_class = SeatCategorySerializer


class ShowtimeList(generics.ListCreateAPIView):
    """
    get: List all the showtimes in future.
    post: Add a new showtime.
    """

    permission_classes = [IsAdminUser]
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer


class MoviesByCity(generics.GenericAPIView):
    serializer_class = MoviesByCitySerialazer

    @swagger_auto_schema(
        operation_summary="Get all movies currently playing in your chosen city, No Authentication required",
        operation_description="Accepts the following POST parameters: city_id, start_date(optional, set to current "
        "date), end_date(optional,set to 7 days later).\nReturn movies list",
        tags=["end-user"],
    )
    def post(self, request):
        payload = request.data
        city = get_object_or_404(City, pk=payload["city"])
        start, end = validate_date_range(payload)
        movies_id = Showtime.objects.filter(
            screen__cinema__city=city, start_timestamp__range=(start, end)
        ).values_list("movie", flat=True)
        movies = Movies.objects.filter(id__in=movies_id)
        return Response(
            MovieSerializer(list(movies), many=True).data, status=status.HTTP_200_OK
        )


class CinemaByMovie(generics.GenericAPIView):
    serializer_class = CinemaByMovieSerializer

    @swagger_auto_schema(
        operation_summary="Get all cinemas where movie is playing, No Authentication required",
        operation_description="Accepts the following POST parameters: "
        "movie_id, city_id, start_date(optional, set to current date), end_date(optional, "
        "set to 7 days later).\nReturn cinemas list along with showtime information",
        tags=["end-user"],
    )
    def post(self, request):
        payload = request.data
        start, end = validate_date_range(payload)
        movie = get_object_or_404(Movies, pk=payload["movie"])
        city = get_object_or_404(City, pk=payload["city"])
        showtimes = Showtime.objects.filter(
            movie=movie,
            screen__cinema__city=city,
            start_timestamp__range=(start, end),
            status="CF",
        )
        screens = Screen.objects.filter(
            id__in=showtimes.values_list("screen", flat=True)
        )
        cinemas = Cinema.objects.filter(id__in=screens.values_list("cinema", flat=True))
        _cinemas = CinemaWithScreensOnly(list(cinemas), many=True).data
        s_ids = showtimes.values_list("id", flat=True)
        resp = list()
        for cinema in _cinemas:
            shows = []
            for co in dict(cinema)["screens"]:
                _shows = list(
                    filter(
                        None,
                        list(filter(lambda d: d["id"] in s_ids, dict(co)["showtimes"])),
                    )
                )
                if len(_shows) > 0:
                    shows.extend(_shows)

            _resp = dict(
                cinema=dict(name=cinema["name"], address=cinema["address"]),
                showtimes=shows,
            )
            resp.append(_resp)

        return Response(resp, status=status.HTTP_200_OK)


class SeatAvailability(generics.RetrieveAPIView):
    lookup_url_kwarg = "showtime_id"
    serializer_class = ReservationSerializer

    @swagger_auto_schema(
        operation_summary="Check availability of showtime, No Authentication required",
        operation_description="Accepts the following GET parameters: showtime_id"
        "\nReturn json response with available seats along with category or message if theatre is full.",
        tags=["end-user"],
    )
    def get(self, request, *args, **kwargs):
        showtime_id = self.kwargs.get(self.lookup_url_kwarg)
        showtime = get_object_or_404(Showtime, pk=showtime_id)

        available_seats = check_availability(showtime)
        if len(available_seats) != 0:
            return Response(
                {"Available Seats": available_seats}, status=status.HTTP_200_OK
            )

        return Response(
            {"Message": "Seats are not available"},
            status=status.HTTP_412_PRECONDITION_FAILED,
        )


class SeatBooking(generics.CreateAPIView):
    serializer_class = SeatBookingSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Book available seat, Authentication is required",
        operation_description="Accepts the following POST parameters: showtime_id, seat_category, seats(no. of seats)"
        "\nReturn json response with booked seats along with reservation metadata or message if seats are not "
        "avaialble at the moment of booking.",
        tags=["end-user"],
    )
    def post(self, request, *args, **kwargs):
        payload = request.data
        user = request.user
        showtime = get_object_or_404(Showtime, pk=payload["showtime_id"], status="CF")
        seat_category = get_object_or_404(SeatCategory, pk=payload["seat_category"])
        logged_in_user = get_object_or_404(CustomUser, email=user)

        available_seats = check_availability(showtime, seat_category)
        if len(available_seats) == 0:
            return Response(
                {"Message": "Seats are not available for given category"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        if available_seats[0]["available_seats"] - int(payload["seats"]) < -1:
            return Response(
                {"Message": "Seats are not available"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        booking = Booking.objects.create(user=logged_in_user)
        reservation = Reservation.objects.create(
            booking=booking,
            showtime=showtime,
            seat_category=seat_category,
            seats=payload["seats"],
        )

        return Response(
            ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED
        )
