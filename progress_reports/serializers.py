from rest_framework import serializers
from .models import ProgressReport, CompletedWork, ProjectTimeline, PlannedWork, ProjectIssues


class CompletedWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedWork
        fields = ['input1', 'input2', 'input3', 'input4']


class ProjectTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTimeline
        fields = ['phase1_status', 'phase2_status', 'phase3_status']


class PlannedWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedWork
        fields = ['input1', 'action1_status', 'due_date1',
                  'input2', 'action2_status', 'due_date2',
                  'input3', 'action3_status', 'due_date3']


class ProjectIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIssues
        fields = ['input1', 'issue1_status',
                  'input2', 'issue2_status',
                  'input3', 'issue3_status']


class ProgressReportSerializer(serializers.ModelSerializer):
    completed_work = CompletedWorkSerializer()
    project_timeline = ProjectTimelineSerializer()
    planned_work = PlannedWorkSerializer()
    project_issues = ProjectIssuesSerializer()

    class Meta:
        model = ProgressReport
        fields = ['completed_work', 'project_timeline', 'planned_work', 'project_issues']