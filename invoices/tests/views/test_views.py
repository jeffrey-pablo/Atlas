from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from invoices.models import Invoice
from invoices.serializers import InvoiceSerializer
from invoices.views import InvoiceViewSet, invoices_table_view, invoices_index_view

class InvoicesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.invoices_table_url = reverse('invoices_table')
        self.invoices_index_url = reverse('invoices_index')
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.invoice_data = {
            'client': 'Client A',
            'description': 'Invoice description',
            'total_hours': 10
        }
        self.invoice = Invoice.objects.create(
            client='Client A',
            description='Invoice description',
            total_hours=10
        )

    def test_invoice_viewset_list(self):
        view = InvoiceViewSet.as_view(actions={'get': 'list'})
        request = self.factory.get('/api/invoices/')
        force_authenticate(request, user=self.user)
        response = view(request)
        queryset = Invoice.objects.all()
        serializer = InvoiceSerializer(queryset, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_invoice_viewset_retrieve(self):
        view = InvoiceViewSet.as_view(actions={'get': 'retrieve'})
        request = self.factory.get('/api/invoices/1/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.invoice.id)
        serializer = InvoiceSerializer(self.invoice)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_invoices_table_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.invoices_table_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoices/invoices_table.html')
        self.assertEqual(response.context['invoices'].count(), 1)
        self.assertEqual(response.context['total_hours'], 10)
        self.assertEqual(response.context['total_amount'], 650)

    def test_invoices_index_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.invoices_index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoices/invoices_index.html')