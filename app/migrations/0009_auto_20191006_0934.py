# Generated by Django 2.2.5 on 2019-10-06 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_player_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_looking_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='is_looking',
            field=models.BooleanField(default=False),
        ),
    ]
