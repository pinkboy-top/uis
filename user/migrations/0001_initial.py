# Generated by Django 3.2 on 2022-01-22 22:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除状态')),
            ],
            options={
                'verbose_name': '基础模型',
                'verbose_name_plural': '基础模型',
                'ordering': ['create_date'],
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.basemodel')),
                ('address_info', models.CharField(max_length=256, verbose_name='详细地址')),
                ('zip_code', models.CharField(max_length=32, verbose_name='邮政编码')),
            ],
            options={
                'verbose_name': '地址信息',
                'verbose_name_plural': '地址信息',
                'ordering': ['create_date'],
            },
            bases=('user.basemodel',),
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.basemodel')),
                ('img_url', models.ImageField(upload_to='uploads/avatar/', verbose_name='图片链接')),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '图片',
                'ordering': ['create_date'],
            },
            bases=('user.basemodel',),
        ),
        migrations.CreateModel(
            name='ImgType',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.basemodel')),
                ('type_name', models.CharField(max_length=256, verbose_name='图片类型名称')),
                ('type_path', models.CharField(max_length=256, verbose_name='类型路径')),
            ],
            options={
                'verbose_name': '图片类型',
                'verbose_name_plural': '图片类型',
                'ordering': ['create_date'],
            },
            bases=('user.basemodel',),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.basemodel')),
                ('option_name', models.CharField(max_length=256, verbose_name='选项名称')),
            ],
            options={
                'verbose_name': '选项',
                'verbose_name_plural': '选项',
                'ordering': ['create_date'],
            },
            bases=('user.basemodel',),
        ),
        migrations.CreateModel(
            name='OptionType',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.basemodel')),
                ('type_name', models.CharField(max_length=256, verbose_name='类型名称')),
            ],
            options={
                'verbose_name': '选项类型',
                'verbose_name_plural': '选项类型',
                'ordering': ['create_date'],
            },
            bases=('user.basemodel',),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='user.basemodel')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='用户ID')),
                ('account', models.CharField(max_length=256, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=512, verbose_name='密码')),
                ('phone', models.CharField(max_length=256, verbose_name='手机号')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['create_date'],
            },
            bases=('user.basemodel',),
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.basemodel')),
                ('nick_name', models.CharField(max_length=256, verbose_name='用户昵称')),
                ('birthday', models.DateTimeField(verbose_name='生日')),
                ('summary', models.CharField(default='没有简介。。。。', max_length=512, verbose_name='用户简介')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='邮箱')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.address', verbose_name='用户地区')),
                ('avatar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.img', verbose_name='用户头像')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.option', verbose_name='性别选项')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='用户信息')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'ordering': ['create_date'],
            },
            bases=('user.basemodel',),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.basemodel')),
                ('region_code', models.CharField(max_length=32, unique=True, verbose_name='行政编码')),
                ('region_name', models.CharField(max_length=64, verbose_name='地区名称')),
                ('region_short_name', models.CharField(max_length=32, null=True, verbose_name='地区缩写')),
                ('region_level', models.IntegerField(verbose_name='地区级别')),
                ('region_parent_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.region', verbose_name='地区父ID')),
            ],
            options={
                'verbose_name': '地区',
                'verbose_name_plural': '地区',
                'ordering': ['create_date'],
            },
            bases=('user.basemodel',),
        ),
        migrations.AddField(
            model_name='option',
            name='option_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.optiontype', verbose_name='选项类型'),
        ),
        migrations.AddField(
            model_name='img',
            name='img_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.imgtype', verbose_name='图片类型'),
        ),
        migrations.AddField(
            model_name='address',
            name='address_tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.option', verbose_name='地址标签'),
        ),
        migrations.AddField(
            model_name='address',
            name='region_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.region', verbose_name='地区'),
        ),
    ]