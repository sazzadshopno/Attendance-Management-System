# Generated by Django 3.0.4 on 2020-03-16 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20200317_0005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batch',
            options={'ordering': ['semester_id']},
        ),
        migrations.RenameField(
            model_name='batch',
            old_name='batch_id',
            new_name='semester_id',
        ),
    ]
