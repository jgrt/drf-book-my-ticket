from django.utils import timezone
from rest_framework import serializers
from .models import (
    City, Brand, Cinema,
    Screen, Movies, SeatCategory,
    ScreenCapacity, Showtime, Booking, Reservation,
    Ticket
)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['id', 'name', 'runtime']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class ScreenCapacitySerializer(serializers.ModelSerializer):
    screen_id = serializers.PrimaryKeyRelatedField(queryset=Screen.objects.all(), source='screen.id')

    class Meta:
        model = ScreenCapacity
        fields = ['id', 'screen_id', 'seat_category', 'no_of_seats', 'cost']

    def create(self, validated_data):
        screen_capacity = ScreenCapacity.objects.create(
            screen=validated_data['screen']['id'],
            seat_category=validated_data['seat_category'],
            no_of_seats=validated_data['no_of_seats'],
            cost=validated_data['cost']
        )
        return screen_capacity


class ShowtimeSerializer(serializers.ModelSerializer):
    screen_id = serializers.PrimaryKeyRelatedField(queryset=Screen.objects.all(), source='screen.id')

    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'screen_id', 'start_timestamp', 'end_timestamp', 'status']

    def validate(self, data):
        booked_show = Showtime.objects.filter(
            screen=data['screen']['id'],
            start_timestamp__in=(data['start_timestamp'], data['end_timestamp']),
            end_timestamp__in=(data['start_timestamp'], data['end_timestamp'])
        )
        total_time = (data['end_timestamp'] - data['start_timestamp']).total_seconds()/60
        if data['start_timestamp'] > data['end_timestamp']:
            raise serializers.ValidationError('end must occur before start')

        if booked_show.exists():
            raise serializers.ValidationError("Another Show already booked on given date and time")

        if Movies.objects.filter(pk=data["movie"].pk).values('runtime')[0]["runtime"] > total_time:
            raise serializers.ValidationError('Movie runtime is greater then selected showtime')

        return data

    def create(self, validated_data):
        showtime = Showtime.objects.create(
            movie=validated_data['movie'],
            screen=validated_data['screen']['id'],
            start_timestamp=validated_data['start_timestamp'],
            end_timestamp=validated_data['end_timestamp']
        )

        return showtime


class ScreenSerializer(serializers.ModelSerializer):
    cinema_id = serializers.PrimaryKeyRelatedField(queryset=Cinema.objects.all(), source='cinema.id')
    screen_capacity = ScreenCapacitySerializer(read_only=True, many=True)
    showtimes = ShowtimeSerializer(many=True, read_only=True, source='available_showtimes') #

    class Meta:
        model = Screen
        fields = ['id', 'name', 'cinema_id', 'screen_capacity', 'showtimes']

    def create(self, validated_data):
        screen = Screen.objects.create(name=validated_data["name"], cinema=validated_data['cinema']['id'])
        return screen


class ScreenWithoutCapacitySerializer(serializers.ModelSerializer):
    cinema_id = serializers.PrimaryKeyRelatedField(queryset=Cinema.objects.all(), source='cinema.id')
    showtimes = ShowtimeSerializer(many=True, read_only=True, source='available_showtimes')  #

    class Meta:
        model = Screen
        fields = ['id', 'name', 'cinema_id', 'showtimes']


class CinemaSerializer(serializers.ModelSerializer):
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='city.id')
    screens = ScreenSerializer(many=True, read_only=True)

    class Meta:
        model = Cinema
        fields = ['id', 'name', 'address', 'brand', 'city_id', 'screens']

    def create(self, validated_data):
        cinema = Cinema.objects.create(
            name=validated_data["name"],
            address=validated_data['address'],
            brand=validated_data['brand'],
            city=validated_data['city']['id']
        )

        return cinema


class CinemaWithScreensOnly(serializers.ModelSerializer):
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='city.id')
    screens = ScreenWithoutCapacitySerializer(many=True, read_only=True)

    class Meta:
        model = Cinema
        fields = ['id', 'name', 'address', 'brand', 'city_id', 'screens']


class CitySerializer(serializers.ModelSerializer):
    cinemas = CinemaSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'cinemas']


class SeatCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatCategory
        fields = ['id', 'name', 'brand']


class ReservationSerializer(serializers.ModelSerializer):
    booking_id = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all(), source='booking.id')
    showtime_id = serializers.PrimaryKeyRelatedField(queryset=Showtime.objects.all(), source='showtime.id')
    seat_category_id = serializers.PrimaryKeyRelatedField(queryset=SeatCategory.objects.all(), source='seat_category.id')

    class Meta:
        model = Reservation
        fields = ['id', 'booking_id', 'showtime_id', 'seat_category_id', 'seats']

    def create(self, validated_data):
        reservation = Reservation.objects.create(
            booking=validated_data['booking']['id'],
            showtime=validated_data['showtime']['id'],
            seat_category=validated_data['seat_category']['id'],
            seats=validated_data['seats']
        )
        return reservation


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'status']


class SeatBookingSerializer(serializers.Serializer):
    showtime_id = serializers.PrimaryKeyRelatedField(queryset=Showtime.objects.all(), source='showtime.id')
    seat_category = serializers.PrimaryKeyRelatedField(queryset=SeatCategory.objects.all(), source='seat_category.id')
    seats = serializers.IntegerField(required=True)


class MoviesByCitySerialazer(serializers.Serializer):
    city = serializers.PrimaryKeyRelatedField(queryset=Cinema.objects.all(), source='city.id')
    start_date = serializers.DateTimeField(default=timezone.now())
    end_date = serializers.DateTimeField(default=timezone.now())


class CinemaByMovieSerializer(serializers.Serializer):
    city = serializers.IntegerField()
    movie = serializers.IntegerField()
    start_date = serializers.DateTimeField(default=timezone.now())
    end_date = serializers.DateTimeField(default=timezone.now())


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'booking', 'amount']