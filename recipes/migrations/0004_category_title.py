# Generated by Django 3.0.4 on 2020-03-23 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20200322_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
