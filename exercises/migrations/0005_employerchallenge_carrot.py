# Generated by Django 3.1.7 on 2021-04-22 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0004_auto_20210422_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerchallenge',
            name='carrot',
            field=models.TextField(default=50, max_length=50),
            preserve_default=False,
        ),
    ]