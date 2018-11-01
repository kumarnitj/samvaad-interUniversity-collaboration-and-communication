# Generated by Django 2.1.2 on 2018-10-31 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_user_name', models.CharField(max_length=100)),
                ('receiver_user_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_user_name', models.CharField(max_length=100)),
                ('receiver_user_name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Newsfeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('interest', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=2000)),
                ('image', models.CharField(max_length=100)),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='basicapp.User_Table')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='basicapp.Newsfeed'),
        ),
    ]
