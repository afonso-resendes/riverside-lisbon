# Generated by Django 3.1.7 on 2022-07-29 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0070_auto_20220728_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservas_coworking_provisoria',
            name='endDate',
        ),
    ]
