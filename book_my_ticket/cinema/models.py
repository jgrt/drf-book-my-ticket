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
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='cinemas')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)


class Screen(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='screens')

    def available_showtimes(self):
        return Showtime.objects.filter(screen=self, start_timestamp__gte=timezone.now())


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
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='screen_capacity')
    seat_category = models.ForeignKey(SeatCategory, on_delete=models.CASCADE)
    no_of_seats = models.IntegerField(blank=False, null=False, default=50)
    cost = models.IntegerField(blank=False, null=False, default=200)


class Showtime(models.Model):
    SHOWTIME_STATUS = (
        ('CF', 'CONFIRMED'),
        ('CC', 'CANCELLED'),
        ('PP', 'POSTPONED')
    )
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='showtimes')
    start_timestamp = models.DateTimeField(blank=False, null=False, default=timezone.now)
    end_timestamp = models.DateTimeField(blank=False, null=False, default=timezone.now)
    status = models.CharField(max_length=2, choices=SHOWTIME_STATUS, default='CF')


class Booking(models.Model):
    BOOKING_STATUS = (
        ('CF', 'CONFIRMED'),
        ('CC', 'CANCELLED'),
        ('PF', 'PAYMENT_FAILED')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=BOOKING_STATUS, default='CF')
    booking_timestamp = models.DateTimeField(default=timezone.now)


class Reservation(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat_category = models.ForeignKey(SeatCategory, on_delete=models.CASCADE)
    seats = models.IntegerField(blank=False, null=False, default=0)


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.FloatField()
