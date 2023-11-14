# Generated by Django 4.2.7 on 2023-11-14 03:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_category_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]