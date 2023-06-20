# Generated by Django 4.2 on 2023-06-02 04:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sessions_timesheets', '0005_session_total_pause_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='total_pause_duration',
            field=models.DurationField(blank=True, default=datetime.timedelta(0), verbose_name='Total Pause Duration'),
        ),
    ]