# Generated by Django 2.1 on 2019-09-11 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_like'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name': 'いいね', 'verbose_name_plural': 'いいね'},
        ),
        migrations.RemoveField(
            model_name='like',
            name='post_id',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user_id',
        ),
        migrations.AlterModelTable(
            name='like',
            table='like',
        ),
    ]