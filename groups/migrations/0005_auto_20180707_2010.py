# Generated by Django 2.0.5 on 2018-07-07 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20180707_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmember',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to='groups.Group'),
        ),
    ]
