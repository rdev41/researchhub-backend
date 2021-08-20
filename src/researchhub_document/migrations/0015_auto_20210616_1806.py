# Generated by Django 2.2 on 2021-06-16 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub_document', '0014_researchhubunifieddocument_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchhubunifieddocument',
            name='paper',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unified_document', to='paper.Paper'),
        ),
    ]