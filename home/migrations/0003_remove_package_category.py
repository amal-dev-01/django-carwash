# Generated by Django 4.2.5 on 2023-10-03 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_slot_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='category',
        ),
    ]