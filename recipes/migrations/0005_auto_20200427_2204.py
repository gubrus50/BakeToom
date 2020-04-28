# Generated by Django 3.0.4 on 2020-04-27 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20200427_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='date_edited',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='date_posted',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='date_posted_old',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Zgadzam się z przectawionymi warunkami i opublikuj mój przepis'),
        ),
    ]
