# Generated by Django 4.2.16 on 2025-01-25 23:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('container_id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('ip_address', models.GenericIPAddressField(protocol='IPv4')),
                ('port', models.SmallIntegerField()),
                ('available', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('init_script', models.FilePathField(path='/root/deploy_scripts')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('device_path', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Device_Reservation',
            fields=[
                ('device_reservation_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.device')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('device_type_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('make', models.CharField(max_length=150)),
                ('model', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('valid_since', models.DateTimeField()),
                ('valid_until', models.DateTimeField()),
                ('root_password', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('PD', 'Pending'), ('IP', 'In progress'), ('FI', 'Finished')], default='PD', max_length=2)),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations_rel', to='backend.container')),
                ('devices', models.ManyToManyField(related_name='reservations', through='backend.Device_Reservation', to='backend.device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offence',
            fields=[
                ('offence_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('commited_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='penalties', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='device_reservation',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.reservation'),
        ),
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.devicetype'),
        ),
    ]