# Generated by Django 4.1.1 on 2022-09-09 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0021_alter_meetingroomprovisoria_endminute_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetingroomprovisoria',
            name='endAm_Pm',
        ),
        migrations.RemoveField(
            model_name='meetingroomprovisoria',
            name='endHour',
        ),
        migrations.RemoveField(
            model_name='meetingroomprovisoria',
            name='endMinute',
        ),
        migrations.RemoveField(
            model_name='meetingroomprovisoria',
            name='startAm_PM',
        ),
        migrations.RemoveField(
            model_name='meetingroomprovisoria',
            name='startHour',
        ),
        migrations.RemoveField(
            model_name='meetingroomprovisoria',
            name='startMinute',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='expire',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='type',
        ),
    ]
