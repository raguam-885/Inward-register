# Generated by Django 5.0.4 on 2024-08-15 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inward', '0002_inward_delete_uploadedfile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inward',
            old_name='inwerd_from',
            new_name='inward_from',
        ),
    ]
