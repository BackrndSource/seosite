# Generated by Django 4.2.7 on 2023-11-25 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_config_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='about',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='contact',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
