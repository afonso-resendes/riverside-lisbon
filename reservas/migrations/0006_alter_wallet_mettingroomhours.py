# Generated by Django 4.0.6 on 2022-08-29 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0005_meetingroomprovisoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='mettingRoomHours',
            field=models.FloatField(default=0.0),
        ),
    ]
