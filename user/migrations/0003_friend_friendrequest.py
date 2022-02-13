# Generated by Django 3.2 on 2022-02-13 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.basemodel')),
                ('request_text', models.CharField(max_length=256, verbose_name='请求留言')),
                ('is_ok', models.BooleanField(default=False, verbose_name='是否处理')),
                ('expired_date', models.DateTimeField(verbose_name='过期日期')),
                ('add_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='add_user', to='user.user', verbose_name='被添加好友')),
                ('request_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_user', to='user.user', verbose_name='请求好友')),
            ],
            options={
                'verbose_name': '好友请求',
                'verbose_name_plural': '好友请求',
                'ordering': ['create_date'],
            },
            bases=('user.basemodel',),
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.basemodel')),
                ('friend', models.ManyToManyField(related_name='friend', to='user.User', verbose_name='好友')),
                ('me', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='me', to='user.user', verbose_name='自己')),
            ],
            options={
                'verbose_name': '好友列表',
                'verbose_name_plural': '好友列表',
                'ordering': ['create_date'],
            },
            bases=('user.basemodel',),
        ),
    ]
