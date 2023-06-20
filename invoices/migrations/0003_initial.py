# Generated by Django 4.1.7 on 2023-05-05 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invoices', '0002_delete_timesheet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_completed', models.DateTimeField(auto_now_add=True)),
                ('total_hours', models.DecimalField(decimal_places=1, max_digits=3)),
            ],
        ),
    ]
