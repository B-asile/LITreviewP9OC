# Generated by Django 4.1.3 on 2022-11-22 08:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_auto_20221118_1420"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="follows",
            field=models.ManyToManyField(
                to=settings.AUTH_USER_MODEL, verbose_name="suit"
            ),
        ),
    ]