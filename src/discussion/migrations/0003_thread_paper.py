# Generated by Django 2.2.5 on 2019-09-19 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0001_initial'),
        ('discussion', '0002_auto_20190918_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='paper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='paper.Paper'),
        ),
    ]