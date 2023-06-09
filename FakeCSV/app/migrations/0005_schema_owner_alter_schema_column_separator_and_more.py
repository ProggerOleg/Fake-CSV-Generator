# Generated by Django 4.1.7 on 2023-03-13 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_alter_schema_column_separator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schema',
            name='column_separator',
            field=models.CharField(choices=[(',', 'Comma (,)'), (';', 'Semicolon (;)'), ('|', 'Pipe (|)'), (' ', 'Space ( )'), ('\\t', 'Tab (   )')], default='Comma (,)', max_length=25),
        ),
        migrations.AlterField(
            model_name='schema',
            name='string_separator',
            field=models.CharField(choices=[('"', 'Double Quote (")'), ("'", "Single Quote (')")], default='Double Quote (")', max_length=25),
        ),
    ]
