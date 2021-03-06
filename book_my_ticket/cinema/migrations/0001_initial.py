# Generated by Django 3.1.1 on 2020-10-08 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CF', 'CONFIRMED'), ('CC', 'CANCELLED'), ('PF', 'PAYMENT_FAILED')], default='CF', max_length=2)),
                ('booking_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=1024)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.brand')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('runtime', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screens', to='cinema.cinema')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('CF', 'CONFIRMED'), ('CC', 'CANCELLED'), ('PP', 'POSTPONED')], default='CF', max_length=2)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.movies')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='showtimes', to='cinema.screen')),
            ],
        ),
        migrations.CreateModel(
            name='SeatCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.brand')),
            ],
        ),
        migrations.CreateModel(
            name='ScreenCapacity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_seats', models.IntegerField(default=50)),
                ('cost', models.IntegerField(default=200)),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screen_capacity', to='cinema.screen')),
                ('seat_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.seatcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.IntegerField(default=0)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.booking')),
                ('seat_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.seatcategory')),
                ('showtime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.showtime')),
            ],
        ),
        migrations.AddField(
            model_name='cinema',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cinemas', to='cinema.city'),
        ),
    ]
