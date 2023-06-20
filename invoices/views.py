from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import permissions, viewsets
from .models import Invoice
from .serializers import InvoiceSerializer
from django.db.models import Sum

# Create your views here.
class InvoiceViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing invoices.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

@login_required(login_url='/accounts/login/')
def invoices_table_view(request):
    invoices = Invoice.objects.all()
    total_hours = invoices.aggregate(total_hours=Sum('total_hours')).get('total_hours', 0)
    rate_dropdown = request.GET.get('rate_dropdown', '65')  # Default value of 65 if not provided
    total_amount = 0

    if rate_dropdown == "65":
        total_amount = total_hours * 65
    elif rate_dropdown == "97.5":
        total_amount = total_hours * 97.5

    context = {
        'invoices': invoices,
        'rate_dropdown': rate_dropdown,
        'total_hours': total_hours,
        'total_amount': total_amount
    }
    return render(request, 'invoices/invoices_table.html', context)

@login_required(login_url='/accounts/login/')
def invoices_index_view(request):
    return render(request, 'invoices/invoices_index.html')
