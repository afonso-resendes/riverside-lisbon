# Generated by Django 3.2 on 2022-06-21 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0043_reservas_coworking_provisoria_qty'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservas_coworking_provisoria',
            old_name='nrLugares',
            new_name='nrPacotes',
        ),
        migrations.RemoveField(
            model_name='reservas_coworking_provisoria',
            name='nrDias',
        ),
        migrations.RemoveField(
            model_name='reservas_coworking_provisoria',
            name='qty',
        ),
    ]
