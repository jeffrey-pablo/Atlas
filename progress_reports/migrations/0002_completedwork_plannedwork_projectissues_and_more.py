# Generated by Django 4.1.7 on 2023-05-18 22:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('progress_reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input1', models.CharField(blank=True, max_length=255)),
                ('input2', models.CharField(blank=True, max_length=255)),
                ('input3', models.CharField(blank=True, max_length=255)),
                ('input4', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PlannedWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input1', models.CharField(blank=True, max_length=255)),
                ('action1_status', models.CharField(choices=[('', 'Not Selected'), ('on-track', 'On Track'), ('not-started', 'Not Started')], max_length=20)),
                ('due_date1', models.DateField(blank=True, null=True)),
                ('input2', models.CharField(blank=True, max_length=255)),
                ('action2_status', models.CharField(choices=[('', 'Not Selected'), ('on-track', 'On Track'), ('not-started', 'Not Started')], max_length=20)),
                ('due_date2', models.DateField(blank=True, null=True)),
                ('input3', models.CharField(blank=True, max_length=255)),
                ('action3_status', models.CharField(choices=[('', 'Not Selected'), ('on-track', 'On Track'), ('not-started', 'Not Started')], max_length=20)),
                ('due_date3', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input1', models.CharField(blank=True, max_length=255)),
                ('issue1_status', models.CharField(choices=[('', 'Not Selected'), ('in-progress', 'In Progress'), ('not-started', 'Not Started')], max_length=20)),
                ('input2', models.CharField(blank=True, max_length=255)),
                ('issue2_status', models.CharField(choices=[('', 'Not Selected'), ('in-progress', 'In Progress'), ('not-started', 'Not Started')], max_length=20)),
                ('input3', models.CharField(blank=True, max_length=255)),
                ('issue3_status', models.CharField(choices=[('', 'Not Selected'), ('in-progress', 'In Progress'), ('not-started', 'Not Started')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTimeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase1_status', models.CharField(choices=[('not-started', 'Not Started'), ('in-progress', 'In Progress'), ('completed', 'Completed')], max_length=20)),
                ('phase2_status', models.CharField(choices=[('not-started', 'Not Started'), ('in-progress', 'In Progress'), ('completed', 'Completed')], max_length=20)),
                ('phase3_status', models.CharField(choices=[('not-started', 'Not Started'), ('in-progress', 'In Progress'), ('completed', 'Completed')], max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='plannedworkdata',
            name='progress_report_model',
        ),
        migrations.RemoveField(
            model_name='projectissuesdata',
            name='progress_report_model',
        ),
        migrations.RemoveField(
            model_name='progressreport',
            name='completed_work',
        ),
        migrations.RemoveField(
            model_name='progressreport',
            name='planned_work',
        ),
        migrations.RemoveField(
            model_name='progressreport',
            name='project_issues',
        ),
        migrations.AddField(
            model_name='progressreport',
            name='report_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.DeleteModel(
            name='CompletedWorkData',
        ),
        migrations.DeleteModel(
            name='PlannedWorkData',
        ),
        migrations.DeleteModel(
            name='ProjectIssuesData',
        ),
        migrations.AddField(
            model_name='projecttimeline',
            name='progress_report_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='progress_reports.progressreport'),
        ),
        migrations.AddField(
            model_name='projectissues',
            name='progress_report_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='progress_reports.progressreport'),
        ),
        migrations.AddField(
            model_name='plannedwork',
            name='progress_report_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='progress_reports.progressreport'),
        ),
        migrations.AddField(
            model_name='completedwork',
            name='progress_report_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='progress_reports.progressreport'),
        ),
    ]