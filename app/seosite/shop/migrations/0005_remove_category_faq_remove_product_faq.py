# Generated by Django 4.2.7 on 2023-11-08 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_category_meta_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='faq',
        ),
        migrations.RemoveField(
            model_name='product',
            name='faq',
        ),
    ]