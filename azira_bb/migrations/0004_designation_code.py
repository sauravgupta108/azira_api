# Generated by Django 3.0.3 on 2020-03-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('azira_bb', '0003_auto_20200226_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='designation',
            name='code',
            field=models.SmallIntegerField(choices=[(41, 'ACTIVE'), (42, 'INACTIVE')], default=101),
        ),
    ]
