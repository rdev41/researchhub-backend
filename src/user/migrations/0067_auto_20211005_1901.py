# Generated by Django 2.2 on 2021-10-05 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0066_auto_20211005_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='access_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to='researchhub_access_group.ResearchhubAccessGroup'),
        ),
    ]