# Generated by Django 5.0.4 on 2024-06-01 07:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(db_index=True, max_length=225)),
                ('department_type', models.CharField(choices=[('Self', 'Self'), ('Aided', 'Aided')], db_index=True, max_length=225)),
            ],
            options={
                'unique_together': {('department_name', 'department_type')},
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(db_index=True, max_length=225)),
                ('role', models.CharField(choices=[('Secretary', 'Secretary'), ('Principal', 'Principal'), ('Initiator', 'Initiator'), ('Office Superintendent', 'Office Superintendent'), ('Department', 'Department')], db_index=True, max_length=225)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('department', models.ForeignKey(blank=True, max_length=225, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
