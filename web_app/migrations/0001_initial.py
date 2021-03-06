# Generated by Django 2.2.5 on 2020-01-10 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_title', models.CharField(max_length=64, verbose_name='公告标题')),
                ('a_content', models.CharField(max_length=3000, null=True, verbose_name='公告内容')),
            ],
            options={
                'verbose_name': '公告表',
                'verbose_name_plural': '公告表',
            },
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k_name', models.CharField(max_length=16, verbose_name='分类名称')),
            ],
            options={
                'verbose_name': '分类表',
                'verbose_name_plural': '分类表',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_tid', models.CharField(max_length=16, verbose_name='帖子id')),
                ('r_uid', models.CharField(max_length=16, verbose_name='发表者id')),
                ('r_photo', models.CharField(max_length=128, null=True, verbose_name='回复的图片')),
                ('r_time', models.DateField(auto_now_add=True, verbose_name='留言时间')),
                ('r_content', models.CharField(max_length=256, verbose_name='回复内容')),
            ],
            options={
                'verbose_name': '回复表',
                'verbose_name_plural': '回复表',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_uid', models.CharField(max_length=16, verbose_name='帖子所属用户id')),
                ('t_kind', models.CharField(max_length=32, verbose_name='类别')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('t_photo', models.CharField(max_length=128, null=True, verbose_name='帖子图片')),
                ('t_content', models.CharField(max_length=3000, verbose_name='帖子正文')),
                ('t_title', models.CharField(max_length=64, verbose_name='帖子标题')),
                ('t_introduce', models.CharField(max_length=256, verbose_name='帖子简介')),
                ('recommend', models.BooleanField(default=False, verbose_name='是否推荐')),
            ],
            options={
                'verbose_name': '帖子表',
                'verbose_name_plural': '帖子表',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, db_index=True, help_text='用户唯一标识', max_length=32, null=True, unique=True, verbose_name='用户id')),
                ('password', models.CharField(max_length=16, verbose_name='密码')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, db_index=True, help_text='用户唯一标识', max_length=32, null=True, unique=True, verbose_name='用户id')),
                ('name', models.CharField(blank=True, db_index=True, help_text='用户姓名', max_length=32, null=True, verbose_name='姓名')),
                ('email', models.CharField(blank=True, db_index=True, help_text='用户邮箱', max_length=40, null=True, verbose_name='邮箱')),
                ('sex', models.IntegerField(choices=[(1, '男'), (0, '女')], default=1, help_text='用户性别', verbose_name='性别')),
                ('age', models.IntegerField(default=0, help_text='用户年龄', verbose_name='年龄')),
                ('nickname', models.CharField(blank=True, help_text='用户昵称', max_length=32, null=True, verbose_name='昵称')),
                ('avatar', models.CharField(blank=True, help_text='用户头像', max_length=60, null=True, verbose_name='头像地址')),
                ('phone', models.CharField(blank=True, db_index=True, help_text='用户电话', max_length=11, null=True, verbose_name='手机号')),
                ('country', models.CharField(blank=True, help_text='用户国家', max_length=32, null=True, verbose_name='国家')),
                ('province', models.CharField(blank=True, help_text='用户省份', max_length=32, null=True, verbose_name='省份')),
                ('city', models.CharField(blank=True, help_text='用户城市', max_length=32, null=True, verbose_name='城市')),
                ('location', models.CharField(blank=True, help_text='用户地址', max_length=60, null=True, verbose_name='地址')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '用户信息表',
                'verbose_name_plural': '用户信息表',
            },
        ),
    ]
