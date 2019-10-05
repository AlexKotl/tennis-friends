# Generated by Django 2.2.5 on 2019-10-05 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20191003_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='court',
            name='image',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='court',
            name='phone',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='court',
            name='url',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=models.CharField(max_length=180),
        ),
        migrations.AlterField(
            model_name='player',
            name='username',
            field=models.CharField(max_length=180),
        ),
    ]