# Generated by Django 2.2.13 on 2020-06-23 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0008_auto_20200214_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='created_location',
            field=models.CharField(blank=True, choices=[('PROGRESS', 'Progress')], default=None, max_length=255, null=True),
        ),
    ]