# Generated by Django 2.2 on 2022-06-10 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub_document', '0037_auto_20220610_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='featuredcontent',
            old_name='hub_id',
            new_name='hub',
        ),
    ]