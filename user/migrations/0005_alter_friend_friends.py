# Generated by Django 3.2.9 on 2022-03-14 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20220314_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='friends',
            field=models.ManyToManyField(related_name='friends', to='user.User', verbose_name='好友'),
        ),
    ]
