# Generated by Django 5.0.1 on 2024-02-14 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_category_options_post_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(default='upload/tech_blog_01.jpg', upload_to='images/'),
        ),
    ]
