# Generated by Django 3.1.5 on 2021-01-12 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='email',
            field=models.EmailField(blank=True, max_length=32),
        ),
    ]
