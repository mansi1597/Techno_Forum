# Generated by Django 2.0.5 on 2018-07-05 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_delete_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='skills',
            field=models.CharField(max_length=300, null=True),
        ),
    ]