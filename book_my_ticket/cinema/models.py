from django.db import models
from django.utils import timezone


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
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
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


class Seat(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    category = models.ForeignKey(SeatCategory, on_delete=models.CASCADE)
    seats = models.IntegerField(blank=False, null=False)


class MovieInCity(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    is_available = models.BooleanField(blank=False, null=False, default=True)




