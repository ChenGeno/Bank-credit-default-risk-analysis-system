# Generated by Django 3.1.4 on 2021-04-08 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_loandata_profile_staffclean'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LoanData',
        ),
        migrations.DeleteModel(
            name='StaffClean',
        ),
    ]