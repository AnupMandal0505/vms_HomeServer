# Generated by Django 5.2 on 2025-04-19 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0010_alter_appointment_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='purpose_of_visit',
            field=models.CharField(default='NA', max_length=100),
        ),
    ]
