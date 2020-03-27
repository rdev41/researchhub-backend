# Generated by Django 2.2.11 on 2020-03-16 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0031_figure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='figure',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='figures', to='paper.Paper'),
        ),
    ]