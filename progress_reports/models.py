from datetime import date
from django.db import models

# Create your models here.
class ProgressReport(models.Model):
        report_title = models.CharField(max_length=255)  # Add the report_title field
        report_date = models.DateField(default=date.today)

        user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True)

        def save(self, *args, **kwargs):
            self.report_title = f"Progress report {self.report_date.strftime('%m/%d/%Y')}"
            super().save(*args, **kwargs)

            # Create related instances
            CompletedWork.objects.create(progress_report_model=self)
            ProjectTimeline.objects.create(progress_report_model=self)
            PlannedWork.objects.create(progress_report_model=self)
            ProjectIssues.objects.create(progress_report_model=self)

        def __str__(self):
            return self.report_title


class CompletedWork(models.Model):
    progress_report_model = models.ForeignKey(ProgressReport, on_delete=models.CASCADE)

    input1 = models.CharField(max_length=255, blank=True, null=True)
    input2 = models.CharField(max_length=255, blank=True, null=True)
    input3 = models.CharField(max_length=255, blank=True, null=True)
    input4 = models.CharField(max_length=255, blank=True, null=True)


class ProjectTimeline(models.Model):
    progress_report_model = models.ForeignKey(ProgressReport, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('not-started', 'Not Started'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    phase1_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    phase2_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    phase3_status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class PlannedWork(models.Model):
    progress_report_model = models.ForeignKey(ProgressReport, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('', 'Not Selected'),  # Option for when nothing is selected
        ('on-track', 'On Track'),
        ('not-started', 'Not Started'),
    ]

    input1 = models.CharField(max_length=255, blank=True, null=True)
    action1_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    due_date1 = models.DateField(null=True, blank=True)

    input2 = models.CharField(max_length=255, blank=True, null=True)
    action2_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    due_date2 = models.DateField(null=True, blank=True)

    input3 = models.CharField(max_length=255, blank=True, null=True)
    action3_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    due_date3 = models.DateField(null=True, blank=True)


class ProjectIssues(models.Model):
    progress_report_model = models.ForeignKey(ProgressReport, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('', 'Not Selected'),  # Option for when nothing is selected
        ('in-progress', 'In Progress'),
        ('not-started', 'Not Started'),
    ]

    input1 = models.CharField(max_length=255, blank=True, null=True)
    issue1_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)

    input2 = models.CharField(max_length=255, blank=True, null=True)
    issue2_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)

    input3 = models.CharField(max_length=255, blank=True, null=True)
    issue3_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)