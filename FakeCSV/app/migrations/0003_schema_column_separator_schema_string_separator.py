# Generated by Django 4.1.7 on 2023-03-12 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_column_name_schema_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='column_separator',
            field=models.CharField(default=',', max_length=15),
        ),
        migrations.AddField(
            model_name='schema',
            name='string_separator',
            field=models.CharField(default=',', max_length=15),
        ),
    ]
