# Generated by Django 5.0.6 on 2024-06-29 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semesterdivision',
            name='department',
        ),
    ]
