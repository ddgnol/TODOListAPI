# Generated by Django 3.1.3 on 2020-11-28 05:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_auto_20201128_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 28, 5, 6, 29, 578700, tzinfo=utc)),
        ),
    ]
