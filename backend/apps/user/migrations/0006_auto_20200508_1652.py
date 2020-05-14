# Generated by Django 3.0.6 on 2020-05-08 16:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200508_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='jwt_secret',
            field=models.UUIDField(default=uuid.UUID('e0ca51bd-5980-43b0-a827-af9e589ba60e'), verbose_name='用户jwt加密秘钥'),
        ),
    ]
