# Generated by Django 4.1 on 2022-08-11 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='static/images')),
                ('caption', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='meetingRooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.CharField(blank=True, choices=[('', ''), ('1', '1'), ('2', '2')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nrLugares', models.IntegerField(default=0)),
                ('startDate', models.DateField(blank=True, null=True)),
                ('endDate', models.DateField(blank=True, null=True)),
                ('nrDias', models.IntegerField(default=0)),
                ('cost_price', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('chair1', models.BooleanField(default=False)),
                ('chair2', models.BooleanField(default=False)),
                ('chair3', models.BooleanField(default=False)),
                ('chair4', models.BooleanField(default=False)),
                ('chair5', models.BooleanField(default=False)),
                ('chair6', models.BooleanField(default=False)),
                ('chair7', models.BooleanField(default=False)),
                ('chair8', models.BooleanField(default=False)),
                ('chair9', models.BooleanField(default=False)),
                ('chair10', models.BooleanField(default=False)),
                ('chair11', models.BooleanField(default=False)),
                ('chair12', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='reservas_Coworking_provisoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField(blank=True, null=True)),
                ('endDate', models.DateField(blank=True, null=True)),
                ('nrDias', models.PositiveIntegerField(default=0)),
                ('cost_price', models.FloatField(default=0.0)),
                ('first_step', models.BooleanField(default=False)),
                ('second_step', models.BooleanField(default=False)),
                ('chair1', models.BooleanField(default=False)),
                ('chair2', models.BooleanField(default=False)),
                ('chair3', models.BooleanField(default=False)),
                ('chair4', models.BooleanField(default=False)),
                ('chair5', models.BooleanField(default=False)),
                ('chair6', models.BooleanField(default=False)),
                ('chair7', models.BooleanField(default=False)),
                ('chair8', models.BooleanField(default=False)),
                ('chair9', models.BooleanField(default=False)),
                ('chair10', models.BooleanField(default=False)),
                ('chair11', models.BooleanField(default=False)),
                ('chair12', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='reservas_Coworking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nrLugares', models.IntegerField(default=0)),
                ('startDate', models.DateField(blank=True, null=True)),
                ('endDate', models.DateField(blank=True, null=True)),
                ('nrDias', models.IntegerField(default=0)),
                ('cost_price', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('chair1', models.BooleanField(default=False)),
                ('chair2', models.BooleanField(default=False)),
                ('chair3', models.BooleanField(default=False)),
                ('chair4', models.BooleanField(default=False)),
                ('chair5', models.BooleanField(default=False)),
                ('chair6', models.BooleanField(default=False)),
                ('chair7', models.BooleanField(default=False)),
                ('chair8', models.BooleanField(default=False)),
                ('chair9', models.BooleanField(default=False)),
                ('chair10', models.BooleanField(default=False)),
                ('chair11', models.BooleanField(default=False)),
                ('chair12', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_price_id', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.product')),
            ],
        ),
        migrations.CreateModel(
            name='mensagens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(null=True)),
                ('ClientName', models.CharField(max_length=30)),
                ('Reason', models.CharField(default='contacto', max_length=50)),
                ('ClientEmail', models.EmailField(default='', max_length=100)),
                ('ClientMessage', models.CharField(max_length=500)),
                ('Pendente', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='meetingRoomCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('sala', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reservas.meetingrooms')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]