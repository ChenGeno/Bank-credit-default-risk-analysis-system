# Generated by Django 3.1.5 on 2021-01-12 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_auto_20210112_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='email',
            field=models.EmailField(max_length=32, null=True),
        ),
    ]
