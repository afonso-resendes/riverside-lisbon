# Generated by Django 4.0.5 on 2022-06-12 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0028_remove_reservas_coworking_valor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservas_coworking',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
