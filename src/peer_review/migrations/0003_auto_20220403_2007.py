# Generated by Django 2.2 on 2022-04-03 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0002_auto_20220403_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='peerreviewdecision',
            old_name='doc_revision',
            new_name='doc_version',
        ),
        migrations.RenameField(
            model_name='peerreviewrequest',
            old_name='doc_revision',
            new_name='doc_version',
        ),
    ]