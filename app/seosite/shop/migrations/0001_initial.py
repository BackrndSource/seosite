# Generated by Django 4.2.7 on 2023-11-06 15:29

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=254, unique=True)),
                ('slug', models.CharField(blank=True, max_length=254, unique=True)),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('meta_description', models.TextField(blank=True, max_length=1000, null=True)),
                ('keywords', models.CharField(blank=True, max_length=254, null=True)),
                ('text', tinymce.models.HTMLField(blank=True, max_length=20000, null=True)),
                ('faq', models.JSONField(blank=True, max_length=20000, null=True)),
                ('featured', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('ext_ref', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, height_field='image_height', null=True, upload_to='', width_field='image_width')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='shop.category')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('value', models.CharField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=254, unique=True)),
                ('slug', models.CharField(blank=True, max_length=254, unique=True)),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('meta_description', models.TextField(blank=True, max_length=1000, null=True)),
                ('keywords', models.CharField(blank=True, max_length=254, null=True)),
                ('text', tinymce.models.HTMLField(blank=True, max_length=20000, null=True)),
                ('faq', models.JSONField(blank=True, max_length=20000, null=True)),
                ('featured', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('ext_ref', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('visible', models.BooleanField(default=True)),
                ('asin', models.CharField(max_length=20, unique=True)),
                ('url', models.URLField(blank=True, max_length=254, null=True)),
                ('url_affiliate', models.URLField(blank=True, max_length=254, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('real_price', models.FloatField(blank=True, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('rating_count', models.IntegerField(blank=True, null=True)),
                ('categories', models.ManyToManyField(blank=True, related_name='products', to='shop.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('author', models.CharField(max_length=64)),
                ('author_img', models.URLField(blank=True, max_length=254, null=True)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(blank=True, max_length=254, null=True)),
                ('thumb', models.URLField(blank=True, max_length=254, null=True)),
                ('large', models.URLField(blank=True, max_length=254, null=True)),
                ('medium', models.URLField(blank=True, max_length=254, null=True)),
                ('small', models.URLField(blank=True, max_length=254, null=True)),
                ('position', models.PositiveSmallIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product')),
            ],
        ),
    ]
