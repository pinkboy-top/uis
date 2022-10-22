# Generated by Django 3.2 on 2022-10-21 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_chat_group_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='bind_user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='绑定用户'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(to='user.User', verbose_name='群成员'),
        ),
    ]