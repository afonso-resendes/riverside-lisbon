# Generated by Django 3.1.7 on 2022-05-12 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_mensagens_pendente'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensagens',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
