from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime

from progress_reports.models import ProgressReport, CompletedWork, ProjectTimeline, PlannedWork, ProjectIssues
from progress_reports.serializers import ProgressReportSerializer
from progress_reports.views import progress_reports_form_view, progress_reports_list_view, progress_reports_confirmation_view, progress_reports_index_view

class ProgressReportsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.form_url = reverse('progress_reports_form')
        self.list_url = reverse('progress_reports_list')
        self.confirmation_url = reverse('progress_reports_confirmation')
        self.index_url = reverse('progress_reports_index')
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword'
        )

    def test_progress_reports_form_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.form_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress_reports/progress_reports_form.html')

        response = self.client.post(self.form_url, {
            'completed_work_1': 'Work 1',
            'completed_work_2': 'Work 2',
            'completed_work_3': 'Work 3',
            'completed_work_4': 'Work 4',
            'phase_1_status': 'Phase 1 status',
            'phase_2_status': 'Phase 2 status',
            'phase_3_status': 'Phase 3 status',
            'planned_work_1': 'Planned work 1',
            'planned_work_1_status': 'Planned work 1 status',
            'due_date_1': '2023-06-20',
            'planned_work_2': 'Planned work 2',
            'planned_work_2_status': 'Planned work 2 status',
            'due_date_2': '2023-06-21',
            'planned_work_3': 'Planned work 3',
            'planned_work_3_status': 'Planned work 3 status',
            'due_date_3': '2023-06-22',
            'project_issue_1': 'Issue 1',
            'project_issue_1_status': 'Issue 1 status',
            'project_issue_2': 'Issue 2',
            'project_issue_2_status': 'Issue 2 status',
            'project_issue_3': 'Issue 3',
            'project_issue_3_status': 'Issue 3 status',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.confirmation_url)

        progress_report = ProgressReport.objects.last()
        completed_work = CompletedWork.objects.get(progress_report_model=progress_report)
        self.assertEqual(completed_work.input1, 'Work 1')
        self.assertEqual(completed_work.input2, 'Work 2')
        self.assertEqual(completed_work.input3, 'Work 3')
        self.assertEqual(completed_work.input4, 'Work 4')

        project_timeline = ProjectTimeline.objects.get(progress_report_model=progress_report)
        self.assertEqual(project_timeline.phase1_status, 'Phase 1 status')
        self.assertEqual(project_timeline.phase2_status, 'Phase 2 status')
        self.assertEqual(project_timeline.phase3_status, 'Phase 3 status')

        planned_work = PlannedWork.objects.get(progress_report_model=progress_report)
        self.assertEqual(planned_work.input1, 'Planned work 1')
        self.assertEqual(planned_work.action1_status, 'Planned work 1 status')
        self.assertEqual(planned_work.due_date1, datetime.strptime('2023-06-20', '%Y-%m-%d').date())
        self.assertEqual(planned_work.input2, 'Planned work 2')
        self.assertEqual(planned_work.action2_status, 'Planned work 2 status')
        self.assertEqual(planned_work.due_date2, datetime.strptime('2023-06-21', '%Y-%m-%d').date())
        self.assertEqual(planned_work.input3, 'Planned work 3')
        self.assertEqual(planned_work.action3_status, 'Planned work 3 status')
        self.assertEqual(planned_work.due_date3, datetime.strptime('2023-06-22', '%Y-%m-%d').date())

        project_issues = ProjectIssues.objects.get(progress_report_model=progress_report)
        self.assertEqual(project_issues.input1, 'Issue 1')
        self.assertEqual(project_issues.issue1_status, 'Issue 1 status')
        self.assertEqual(project_issues.input2, 'Issue 2')
        self.assertEqual(project_issues.issue2_status, 'Issue 2 status')
        self.assertEqual(project_issues.input3, 'Issue 3')
        self.assertEqual(project_issues.issue3_status, 'Issue 3 status')

    def test_progress_reports_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress_reports/progress_reports_list.html')

    def test_progress_reports_confirmation_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.confirmation_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress_reports/progress_reports_confirmation.html')

    def test_progress_reports_index_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress_reports/progress_reports_index.html')