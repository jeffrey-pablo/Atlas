from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from .serializers import ProgressReportSerializer
from .models import ProgressReport, CompletedWork, ProjectTimeline, PlannedWork, ProjectIssues

# Create your views here.
class ProgressReportViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing progress reports.
    """
    queryset = ProgressReport.objects.all()
    serializer_class = ProgressReportSerializer
    permission_classes = [permissions.IsAuthenticated]

@login_required(login_url='/accounts/login/')
def progress_reports_form_view(request):
    if request.method == 'POST':
        user = request.user
        # Create a new ProgressReport instance
        progress_report = ProgressReport.objects.create(user=user)

        # Fetch CompletedWork instance and set the input values
        completed_work = CompletedWork.objects.get(progress_report_model=progress_report)
        completed_work.input1 = request.POST.get('completed_work_1')
        completed_work.input2 = request.POST.get('completed_work_2')
        completed_work.input3 = request.POST.get('completed_work_3')
        completed_work.input4 = request.POST.get('completed_work_4')
        completed_work.save()

        # Fetch ProjectTimeline instance and set the status values
        project_timeline = ProjectTimeline.objects.get(progress_report_model=progress_report)
        project_timeline.phase1_status = request.POST.get('phase_1_status')
        project_timeline.phase2_status = request.POST.get('phase_2_status')
        project_timeline.phase3_status = request.POST.get('phase_3_status')
        project_timeline.save()

        # Fetch PlannedWork instance and set the input, status, and due date values
        planned_work = PlannedWork.objects.get(progress_report_model=progress_report)
        planned_work.input1 = request.POST.get('planned_work_1')
        planned_work.action1_status = request.POST.get('planned_work_1_status')
        due_date_1 = request.POST.get('due_date_1')
        planned_work.due_date1 = datetime.strptime(due_date_1, '%Y-%m-%d').date() if due_date_1 else None
        planned_work.input2 = request.POST.get('planned_work_2')
        planned_work.action2_status = request.POST.get('planned_work_2_status')
        due_date_2 = request.POST.get('due_date_2')
        planned_work.due_date2 = datetime.strptime(due_date_2, '%Y-%m-%d').date() if due_date_2 else None
        planned_work.input3 = request.POST.get('planned_work_3')
        planned_work.action3_status = request.POST.get('planned_work_3_status')
        due_date_3 = request.POST.get('due_date_3')
        planned_work.due_date3 = datetime.strptime(due_date_3, '%Y-%m-%d').date() if due_date_3 else None
        planned_work.save()


        # Fetch ProjectIssues instance and set the input and status values
        project_issues = ProjectIssues.objects.get(progress_report_model=progress_report)
        project_issues.input1 = request.POST.get('project_issue_1')
        project_issues.issue1_status = request.POST.get('project_issue_1_status')
        project_issues.input2 = request.POST.get('project_issue_2')
        project_issues.issue2_status = request.POST.get('project_issue_2_status')
        project_issues.input3 = request.POST.get('project_issue_3')
        project_issues.issue3_status = request.POST.get('project_issue_3_status')
        project_issues.save()

        # Redirect to a success page or perform any other actions
        return redirect('progress_reports_confirmation')

    # If the request method is not POST, render the progress report template
    return render(request, 'progress_reports/progress_reports_form.html')

@login_required(login_url='/accounts/login/')
def progress_reports_list_view(request):
    # Retrieve the progress reports from the database
    user = request.user
    progress_reports = ProgressReport.objects.filter(user=user)

    # Create a context dictionary with the progress reports
    context = {
        'progress_reports': progress_reports
    }

    # Render the template with the context data
    return render(request, 'progress_reports/progress_reports_list.html', context)


@login_required(login_url='/accounts/login/')
def progress_reports_confirmation_view(request):
    # Logic for handling the success page
    return render(request, 'progress_reports/progress_reports_confirmation.html')

@login_required(login_url='/accounts/login/')
def progress_reports_index_view(request):
    # Logic for handling the success page
    return render(request, 'progress_reports/progress_reports_index.html')