# Generated by Django 5.1.2 on 2025-02-21 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_feudquestion_game_feudanswer_round'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FamilyFeudGameProperCenter',
        ),
        migrations.DeleteModel(
            name='FamilyFeudGameProperLeft',
        ),
        migrations.DeleteModel(
            name='FamilyFeudGameProperMaam',
        ),
        migrations.DeleteModel(
            name='FamilyFeudGameProperRight',
        ),
    ]
