# Generated by Django 3.0.7 on 2020-06-10 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
