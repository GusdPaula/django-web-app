# Generated by Django 5.0.3 on 2024-03-25 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boost', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expenses',
            name='user',
        ),
        migrations.AlterField(
            model_name='expenses',
            name='amount',
            field=models.FloatField(null=True),
        ),
    ]
