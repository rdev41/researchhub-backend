# Generated by Django 2.2 on 2022-04-20 23:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hub', '0019_remove_hubmembership_created_at'),
        ('paper', '0092_auto_20220330_1824'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsyncPaperUpdator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('doi', models.CharField(blank=True, default=None, help_text='May be either extracted / user uploaded doi', max_length=255, null=True, unique=True)),
                ('title', models.CharField(help_text='User generated title', max_length=1024)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('hubs', models.ManyToManyField(to='hub.Hub')),
                ('paper_submission', models.OneToOneField(help_text='Self-explanatory', on_delete=django.db.models.deletion.CASCADE, related_name='async_upadtor', to='paper.PaperSubmission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]