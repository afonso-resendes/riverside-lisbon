# Generated by Django 3.2 on 2022-06-22 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0047_reservas_coworking_provisoria_second_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservas_coworking_provisoria',
            name='nrPacotes',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
