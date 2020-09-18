from django.db import models
from django.utils import timezone

from auth_app.models import CustomUser


class City(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)


class Brand(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)


class Cinema(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    address = models.CharField(max_length=1024, blank=False, null=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)


class Screen(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)


class Movies(models.Model):
    '''
       TODO Add language and other movie fields
    '''
    name = models.CharField(max_length=512, blank=False, null=False)
    runtime = models.IntegerField(blank=False, null=False)


class SeatCategory(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)


class ScreenCapacity(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    seat_category = models.ForeignKey(SeatCategory, on_delete=models.CASCADE)
    no_of_seats = models.IntegerField(blank=False, null=False, default=50)
    cost = models.IntegerField(blank=False, null=False, default=200)


class Showtime(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=False, null=False, default=timezone.now)


class Booking(models.Model):
    BOOKING_STATUS = (
        ('CF', 'CONFIRMED'),
        ('CC', 'CANCELLED'),
        ('PF', 'PAYMENT_FAILED')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat_category = models.ForeignKey(SeatCategory, on_delete=models.CASCADE)
    seats = models.IntegerField(blank=False, null=False)
    status = models.CharField(max_length=2, choices=BOOKING_STATUS)


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.FloatField()





