# Generated by Django 2.0.4 on 2018-12-07 12:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20181207_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='accessdb',
        ),
        migrations.AlterField(
            model_name='users',
            name='jwt_secret',
            field=models.UUIDField(default=uuid.UUID('96833a1b-a89a-41b2-a5aa-a17672a0a149'), verbose_name='用户jwt加密秘钥'),
        ),
    ]