# Generated by Django 4.1.1 on 2022-09-09 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservas', '0015_bundleprovisorio'),
    ]

    operations = [
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('', ''), ('1', '1'), ('2', '2')], max_length=50, null=True)),
                ('status', models.CharField(choices=[('', ''), ('1', '1'), ('2', '2')], max_length=50, null=True)),
                ('expire', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
