# Generated by Django 3.1.3 on 2020-11-28 02:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_auto_20201127_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 28, 2, 52, 41, 178178, tzinfo=utc)),
        ),
    ]