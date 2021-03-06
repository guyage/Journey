# Generated by Django 3.0.6 on 2020-05-08 16:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200508_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='jwt_secret',
            field=models.UUIDField(default=uuid.UUID('ef2da108-3f17-48ed-a2b5-aabc2e2aebad'), verbose_name='用户jwt加密秘钥'),
        ),
    ]
