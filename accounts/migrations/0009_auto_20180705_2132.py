# Generated by Django 2.0.5 on 2018-07-05 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20180705_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='profile_pic',
            field=models.ImageField(default='1.png', upload_to='profile_pics'),
        ),
    ]
