# Generated by Django 2.2.5 on 2019-10-09 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20191006_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='image_url',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
