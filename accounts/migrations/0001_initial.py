# Generated by Django 5.0 on 2024-01-04 04:24

import accounts.validators
import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=50, validators=[accounts.validators.validate_name], verbose_name='Name')),
                ('last_name', models.CharField(max_length=50, validators=[accounts.validators.validate_name], verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('mobile_phone', models.CharField(unique=True, validators=[accounts.validators.validate_mobile_phone], verbose_name='Mobile Phone')),
                ('role', models.CharField(choices=[('P', 'Project Manager'), ('D', 'Developer')], default='D', max_length=1, verbose_name='Role')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=50, validators=[accounts.validators.validate_name], verbose_name='Name')),
                ('last_name', models.CharField(max_length=50, validators=[accounts.validators.validate_name], verbose_name='Last Name')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='Email')),
                ('mobile_phone', models.CharField(db_index=True, validators=[accounts.validators.validate_mobile_phone], verbose_name='Mobile Phone')),
                ('role', models.CharField(choices=[('P', 'Project Manager'), ('D', 'Developer')], default='D', max_length=1, verbose_name='Role')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(blank=True, editable=False)),
                ('last_update', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical User',
                'verbose_name_plural': 'historical Users',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]