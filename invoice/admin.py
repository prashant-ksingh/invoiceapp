from django.contrib import admin
from invoice import views

admin.site.register(views.Invoice),
admin.site.register(views.InvoiceDetail),
