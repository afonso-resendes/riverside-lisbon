# Generated by Django 4.1.1 on 2022-09-09 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0022_remove_meetingroomprovisoria_endam_pm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payment_Method',
            field=models.CharField(choices=[('', ''), ('MBWAY', 'MBWAY'), ('REFERENCE', 'REFERENCE'), ('CARD', 'CARD')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]