# Generated by Django 3.0.4 on 2020-03-20 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_auto_20200319_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='username',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]