# Generated by Django 5.0.1 on 2024-02-14 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(default='defaults.jpg', upload_to='images/'),
        ),
    ]
