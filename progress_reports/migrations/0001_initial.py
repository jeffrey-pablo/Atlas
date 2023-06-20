# Generated by Django 4.1.7 on 2023-05-13 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProgressReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_work', models.TextField()),
                ('planned_work', models.TextField()),
                ('project_issues', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectIssuesData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_issues_input', models.CharField(max_length=2048, null=True)),
                ('progress_report_model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='progress_reports.progressreport')),
            ],
        ),
        migrations.CreateModel(
            name='PlannedWorkData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planned_work_input', models.CharField(max_length=2048, null=True)),
                ('progress_report_model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='progress_reports.progressreport')),
            ],
        ),
        migrations.CreateModel(
            name='CompletedWorkData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_work_input', models.CharField(max_length=2048, null=True)),
                ('progress_report_model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='progress_reports.progressreport')),
            ],
        ),
    ]