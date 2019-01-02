# Generated by Django 2.0.4 on 2018-12-04 11:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20181203_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='jwt_secret',
            field=models.UUIDField(default=uuid.UUID('b6603f16-9115-402a-ba28-326716a09404'), verbose_name='用户jwt加密秘钥'),
        ),
    ]
