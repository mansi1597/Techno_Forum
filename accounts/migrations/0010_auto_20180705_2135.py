# Generated by Django 2.0.5 on 2018-07-05 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20180705_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='profile_pic',
            field=models.ImageField(default='1.jpg', upload_to='profile_pics'),
        ),
    ]