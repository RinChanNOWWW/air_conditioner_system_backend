# Generated by Django 3.0.3 on 2020-04-17 11:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomStatus',
            fields=[
                ('room_id', models.IntegerField(primary_key=True, serialize=False)),
                ('ac_status', models.CharField(default='Off', max_length=10)),
                ('temperature', models.DecimalField(decimal_places=1, default=25.0, max_digits=3)),
                ('target_temp', models.DecimalField(decimal_places=1, default=25.0, max_digits=3)),
                ('check_in_time', models.DateTimeField(blank=True, null=True)),
                ('last_change_time', models.DateTimeField(blank=True, null=True)),
                ('online_time', models.DurationField(default=0)),
                ('electricity_now', models.IntegerField(default=datetime.timedelta(0))),
            ],
        ),
        migrations.CreateModel(
            name='RoomLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.IntegerField()),
                ('check_in_time', models.DateTimeField()),
                ('timestamp', models.DateTimeField()),
                ('temperature', models.DecimalField(decimal_places=1, max_digits=3)),
                ('ac_status', models.CharField(max_length=10)),
                ('electricity_now', models.IntegerField(default=0)),
            ],
            options={
                'unique_together': {('room_id', 'check_in_time', 'timestamp')},
            },
        ),
        migrations.CreateModel(
            name='RoomCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.IntegerField()),
                ('check_in_time', models.DateTimeField()),
                ('check_out_time', models.DateTimeField(blank=True, null=True)),
                ('electricity_now', models.IntegerField(default=0)),
            ],
            options={
                'unique_together': {('room_id', 'check_in_time')},
            },
        ),
    ]