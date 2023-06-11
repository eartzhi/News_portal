# Generated by Django 4.2.1 on 2023-06-10 15:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_category_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscriber',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='category_subscriber'),
        ),
    ]
