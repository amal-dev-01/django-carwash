# Generated by Django 4.2.5 on 2023-10-03 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='expiration_date',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='is_used',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='users',
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_percentage',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coupon',
            name='valid_for_first_login',
            field=models.BooleanField(default=True),
        ),
    ]
