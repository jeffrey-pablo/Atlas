from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from sessions_timesheets.models.sessions import Session
from sessions_timesheets.serializers import SessionSerializer
from sessions_timesheets.views import (
    SessionViewSet,
    calculate_day_of_week,
    sessions_form_view,
    sessions_index_view,
    sessions_detail_view,
    total_hours_to_float,
    timesheets_table_view,
    timesheets_index_view,
)

class SessionsTimesheetsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.sessions_list_url = reverse('session-list')
        self.sessions_detail_url = reverse('session-detail', kwargs={'pk': 1})
        self.current_session_url = reverse('session-current_session')
        self.timesheets_table_url = reverse('timesheets-table')
        self.timesheets_index_url = reverse('timesheets-index')
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.session_data = {
            'time_in': '2023-06-20T09:00:00Z',
            'active': True
        }
        self.session = Session.objects.create(
            user=self.user,
            time_in='2023-06-20T09:00:00Z',
            active=True
        )

    def test_session_viewset_list(self):
        view = SessionViewSet.as_view(actions={'get': 'list'})
        factory = APIRequestFactory()
        request = factory.get('/sessions/')
        force_authenticate(request, user=self.user)
        response = view(request)
        queryset = Session.objects.filter(user=self.user)
        serializer = SessionSerializer(queryset, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_session_viewset_retrieve(self):
        view = SessionViewSet.as_view(actions={'get': 'retrieve'})
        factory = APIRequestFactory()
        request = factory.get('/sessions/1/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.session.id)
        serializer = SessionSerializer(self.session)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_session_viewset_current_session_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.current_session_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = SessionSerializer(self.session)
        self.assertEqual(response.data, serializer.data)

    def test_session_viewset_current_session_patch_pause(self):
        self.client.force_login(self.user)
        response = self.client.patch(self.current_session_url, data={
            'id': self.session.id,
            'pause_timestamp': '2023-06-20T10:00:00Z',
            'action': 'pause',
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.session.refresh_from_db()
        self.assertTrue(self.session.paused)
        self.assertEqual(str(self.session.pause_start), '2023-06-20 10:00:00+00:00')

    def test_session_viewset_current_session_patch_continue(self):
        self.session.paused = True
        self.session.pause_start = '2023-06-20T10:00:00Z'
        self.session.save()

        self.client.force_login(self.user)
        response = self.client.patch(self.current_session_url, data={
            'id': self.session.id,
            'continue_timestamp': '2023-06-20T11:00:00Z',
            'action': 'continue',
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.session.refresh_from_db()
        self.assertFalse(self.session.paused)
        self.assertEqual(str(self.session.paused_end), '2023-06-20 11:00:00+00:00')

    def test_session_viewset_current_session_patch_end(self):
        self.session.active = True
        self.session.time_in = '2023-06-20T09:00:00Z'
        self.session.total_pause_duration = timedelta(hours=1)
        self.session.save()

        self.client.force_login(self.user)
        response = self.client.patch(self.current_session_url, data={
            'id': self.session.id,
            'end_timestamp': '2023-06-20T12:00:00Z',
            'action': 'end',
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.session.refresh_from_db()
        self.assertFalse(self.session.active)
        self.assertEqual(str(self.session.time_out), '2023-06-20 12:00:00+00:00')

    def test_session_viewset_post_current_session(self):
        self.client.force_login(self.user)
        response = self.client.post(self.current_session_url, data=self.session_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Session.objects.count(), 2)

    def test_sessions_form_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('sessions-form'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'sessions_timesheets/sessions_form.html')

        response = self.client.post(reverse('sessions-form'), data={
            'task': 'Task 1',
            'description': 'Description 1',
            'total_hours': 5
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.count(), 1)
        invoice = Invoice.objects.first()
        self.assertEqual(invoice.task, 'Task 1')
        self.assertEqual(invoice.description, 'Description 1')
        self.assertEqual(invoice.total_hours, 5)

    def test_sessions_index_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('sessions-index'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'sessions_timesheets/sessions_index.html')

    def test_sessions_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('sessions-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'sessions_timesheets/sessions_detail.html')

    def test_timesheets_table_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('timesheets-table'), data={'week_number': 25})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'sessions_timesheets/timesheets_table.html')

    def test_timesheets_index_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('timesheets-index'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'sessions_timesheets/timesheets_index.html')

    def test_calculate_day_of_week(self):
        time_in_str = '2023-06-20T09:00:00Z'
        day_of_week, date_str = calculate_day_of_week(time_in_str)
        self.assertEqual(day_of_week, 'Tuesday')
        self.assertEqual(date_str, '2023-06-20')

    def test_total_hours_to_float(self):
        total_hours = timedelta(hours=2, minutes=30)
        total_hours_float = total_hours_to_float(total_hours)
        self.assertEqual(total_hours_float, 2.5)