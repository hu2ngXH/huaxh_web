# Generated by Django 2.1.8 on 2019-06-11 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.CharField(max_length=100, verbose_name='评论目标'),
        ),
    ]
