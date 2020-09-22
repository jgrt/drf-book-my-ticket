from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
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


class CinemaViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            email="gandalf@lotr.com", password="gandalfthegray"
        )
        self.city = City.objects.create(name="Auckland")
        self.brand = Brand.objects.create(name="Bridgeway")
        self.cinema = Cinema.objects.create(
            name="Bridgeway",
            address="122 Queen St, Northcote Point",
            city_id=self.city.pk,
            brand=self.brand,
        )
        self.screen = Screen.objects.create(name="AUD_101", cinema_id=self.cinema.pk)
        self.seat_category_1 = SeatCategory.objects.create(
            name="Platinum", brand=self.brand
        )
        self.seat_category_2 = SeatCategory.objects.create(
            name="Gold", brand=self.brand
        )
        self.seat_category_3 = SeatCategory.objects.create(
            name="Silver", brand=self.brand
        )
        self.screen1_category1_capacity = ScreenCapacity.objects.create(
            screen_id=self.screen.pk,
            seat_category=self.seat_category_1,
            no_of_seats=30,
            cost=100,
        )
        self.screen1_category2_capacity = ScreenCapacity.objects.create(
            screen_id=self.screen.pk,
            seat_category=self.seat_category_2,
            no_of_seats=50,
            cost=50,
        )
        self.screen1_category3_capacity = ScreenCapacity.objects.create(
            screen_id=self.screen.pk,
            seat_category=self.seat_category_3,
            no_of_seats=170,
            cost=20,
        )
        self.movie1 = Movies.objects.create(name="Tenet", runtime=150)
        self.movie2 = Movies.objects.create(name="Savage", runtime=100)
        self.showtime1 = Showtime.objects.create(
            movie=self.movie1,
            screen_id=self.screen.pk,
            start_timestamp="2020-09-23T17:00:00.000Z",
            end_timestamp="2020-09-23T20:45:00.000Z",
        )
        self.showtime2 = Showtime.objects.create(
            movie=self.movie2,
            screen_id=self.screen.pk,
            start_timestamp="2020-09-24T12:00:00.000Z",
            end_timestamp="2020-09-24T13:45:00.000Z",
        )

    def test_movies_in_city(self):
        url = "/api/v1/movies_by_city/"
        data = {
            "city": self.city.pk,
            "start_date": "2020-09-22T20:19:18.151Z",
            "end_date": "2020-09-25T17:19:18.151Z",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data, "Must be empty list if no movies found")

    def test_movies_in_cinema(self):
        url = "/api/v1/cinema_by_movie/"
        data = {
            "city": self.city.pk,
            "movie": self.movie1.pk,
            "start_date": "2020-09-22T20:19:18.151Z",
            "end_date": "2020-09-25T17:19:18.151Z",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data, "Must be empty list if no cinema found")

    def test_seat_availability(self):
        showtime_id = self.showtime1.pk
        url = f"/api/v1/check_seat_availability/{showtime_id}/"
        response = self.client.get(url)
        self.assertIsNotNone(response.data)

    def test_seat_booking(self):
        self.client.force_login(user=self.user)
        url = "/api/v1/book_seat/"
        data = {
            "showtime_id": self.showtime1.pk,
            "seat_category": self.seat_category_1.pk,
            "seats": 2,
        }
        response = self.client.post(url, data)
        self.assertIsNotNone(response.data)
