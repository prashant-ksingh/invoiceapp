# from django.urls import path, include
# from .views import InvoiceViewSet, InvoiceDetailViewSet

from django.urls import path
# from invoice import views
from .views import *

urlpatterns = [
    path('invoices/', getInvoice_f),
    path('invoices/<int:pk>/', getInvoicepk_f),
    path('createupdateinvoices/<int:pk>/', createupdateinvoices_f),
]