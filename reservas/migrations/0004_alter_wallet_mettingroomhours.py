# Generated by Django 4.0.6 on 2022-08-22 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_alter_wallet_mettingroomhours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='mettingRoomHours',
            field=models.IntegerField(default=0),
        ),
    ]
