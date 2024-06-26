# Generated by Django 5.0.1 on 2024-04-07 05:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_set', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_to_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='app_account.Contact', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['-created'], name='app_account_created_04ed4f_idx'),
        ),
    ]
