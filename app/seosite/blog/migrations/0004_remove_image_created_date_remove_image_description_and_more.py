# Generated by Django 4.2.7 on 2023-11-19 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='image',
            name='description',
        ),
        migrations.RemoveField(
            model_name='image',
            name='ext_ref',
        ),
        migrations.RemoveField(
            model_name='image',
            name='featured',
        ),
        migrations.RemoveField(
            model_name='image',
            name='keywords',
        ),
        migrations.RemoveField(
            model_name='image',
            name='last_modified',
        ),
        migrations.RemoveField(
            model_name='image',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='image',
            name='publish_date',
        ),
        migrations.RemoveField(
            model_name='image',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='image',
            name='text',
        ),
        migrations.RemoveField(
            model_name='image',
            name='title',
        ),
        migrations.RemoveField(
            model_name='image',
            name='visible',
        ),
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(blank=True, default='New Image', max_length=100, null=True),
        ),
    ]