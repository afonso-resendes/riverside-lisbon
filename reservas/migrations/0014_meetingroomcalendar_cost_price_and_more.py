# Generated by Django 4.1.1 on 2022-09-07 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0013_alter_reservas_coworking_cost_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingroomcalendar',
            name='cost_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='meetingroomprovisoria',
            name='cost_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='meetingroomprovisoria',
            name='transactionId',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
