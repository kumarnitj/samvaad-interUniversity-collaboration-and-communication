# Generated by Django 2.1.2 on 2018-12-24 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicapp', '0014_auto_20181220_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsfeedScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('score', models.CharField(max_length=20)),
                ('newsfeed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicapp.Newsfeed')),
            ],
        ),
    ]
