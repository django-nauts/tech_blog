# Generated by Django 5.0.1 on 2024-04-11 18:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_comment_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, default=0, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]
