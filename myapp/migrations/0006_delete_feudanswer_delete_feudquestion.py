# Generated by Django 5.1.6 on 2025-02-23 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_feudquestion_flag'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FeudAnswer',
        ),
        migrations.DeleteModel(
            name='FeudQuestion',
        ),
    ]
