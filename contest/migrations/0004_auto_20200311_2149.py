# Generated by Django 2.1 on 2020-03-12 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_taskmanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmanager',
            name='end_at',
            field=models.DateTimeField(null=True, verbose_name='date end'),
        ),
    ]
