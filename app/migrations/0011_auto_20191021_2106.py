# Generated by Django 2.2.5 on 2019-10-21 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_player_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='image',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='court',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='court',
            name='url',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='player',
            name='about',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='player',
            name='courts',
            field=models.ManyToManyField(blank=True, to='app.Court'),
        ),
        migrations.AlterField(
            model_name='player',
            name='image_url',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=models.CharField(blank=True, max_length=180),
        ),
    ]
