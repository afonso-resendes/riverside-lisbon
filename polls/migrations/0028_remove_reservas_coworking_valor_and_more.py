# Generated by Django 4.0.5 on 2022-06-07 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0027_alter_calendar_id_alter_chair_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservas_coworking',
            name='valor',
        ),
        migrations.AddField(
            model_name='reservas_coworking',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservas_coworking',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='reservas_coworking',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
