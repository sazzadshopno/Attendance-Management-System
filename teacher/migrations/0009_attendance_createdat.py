# Generated by Django 4.1.1 on 2022-09-20 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0008_alter_attendance_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='createdAt',
            field=models.DateTimeField(auto_created=True, auto_now=True),
        ),
    ]
