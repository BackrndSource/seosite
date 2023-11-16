# Generated by Django 4.2.7 on 2023-11-16 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_category_keywords_alter_product_keywords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='config',
            name='value',
        ),
        migrations.AddField(
            model_name='config',
            name='blog_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='config',
            name='blog_theme',
            field=models.CharField(default='blog', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='config',
            name='canonical_url',
            field=models.URLField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='config',
            name='shop_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='config',
            name='shop_theme',
            field=models.CharField(default='giftos', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='config',
            name='title_decorator',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='config',
            name='title_home',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]