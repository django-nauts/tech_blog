# Generated by Django 5.0.1 on 2024-04-08 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
    ]