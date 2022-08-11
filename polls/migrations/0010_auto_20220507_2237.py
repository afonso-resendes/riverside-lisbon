# Generated by Django 3.1.7 on 2022-05-07 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20220507_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='chair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.CharField(blank=True, choices=[('', ''), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='calendar',
            name='lugar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.chair'),
        ),
    ]
