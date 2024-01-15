from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Invoice, InvoiceDetail
from .serializers import *


@api_view(['GET'])
def getInvoice_f(request):
    try:
            
            print("##########3",request.data)

            all_invoices = Invoice.objects.all()
            invoice_serializer = GetInvoiceSerializer(all_invoices, many=True)

            all_invoice_details = InvoiceDetail.objects.all()
            invoice_detail_serializer = GETInvoicedetailSerializer(all_invoice_details, many=True)

            if invoice_serializer and invoice_detail_serializer  :

                invoice_dict = {}
                for invoice_detail in invoice_detail_serializer.data:
                    invoice_id = invoice_detail['invoice']
                    if invoice_id not in invoice_dict:
                        invoice_dict[invoice_id] = {'id': invoice_id, 'details': []}
                    invoice_dict[invoice_id]['details'].append(invoice_detail)

                formatted_data = []
                for invoice_data in invoice_serializer.data:
                    invoice_id = invoice_data['id']
                    if invoice_id in invoice_dict:
                        formatted_data.append({
                            'invoice': invoice_data,
                            'invoice_details': invoice_dict[invoice_id]['details']
                        })

                json_data = {
                    'status_code': 200,
                    'status': 'Success',
                    'data': formatted_data,
                    'message': 'Got Invoice detail'
                }
                return Response(json_data, status=status.HTTP_200_OK)
            else :
                json_data = {
                    'status_code': 200,
                    'status': 'fail',
                    'data': 'Failed to update invoice detail'
                }
                return Response(json_data, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error --------:", e)
        json_data = {
            'status_code': 400,
            'status': 'Fail',
            'Reason': e,
            'Remark': 'landed in exception',
        }
        raise APIException(json_data, code=status.HTTP_500_INTERNAL_SERVER_ERROR)
from django.shortcuts import get_object_or_404    


@api_view(['GET'])
def getInvoicepk_f(request,pk):
    try:
            invoice = Invoice.objects.get(pk=pk)
            invoice_serializer = GetInvoiceSerializer(invoice)

            all_invoice_details = InvoiceDetail.objects.get(pk=pk)
            invoice_detail_serializer = GETInvoicedetailSerializer(all_invoice_details)
            
            json_data = {
                'status_code': 200,
                'status': 'got invoice',
                'invoice': invoice_serializer.data,
                'invoice_detail': invoice_detail_serializer.data,
                'data': 'Successfully retrieved invoice detail'
            }
            return Response(json_data, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error --------:", e)
        json_data = {
            'status_code': 400,
            'status': 'Fail',
            'Reason': e,
            'Remark': 'landed in exception',
        }
        raise APIException(json_data, code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def createupdateinvoices_f(request, pk):
    try:
        invoice_instance = Invoice.objects.get(pk=pk)

        invoice_detail_instance, created = InvoiceDetail.objects.get_or_create(invoice=invoice_instance)

        if created:
            invoice_detail_instance.description = 'Product ABC'
            invoice_detail_instance.quantity = 5
            invoice_detail_instance.unit_price = 10.50
            invoice_detail_instance.price = 52.50
        else:
            serializer = InvoiceDetailSerializer(instance=invoice_detail_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        json_data = {
            'status_code': 200,
            'status': 'Success',
            'data': 'Invoice detail updated/created successfully',
        }
        return Response(json_data, status=status.HTTP_200_OK)

    except Invoice.DoesNotExist:
        json_data = {
            'status_code': 404,
            'status': 'Fail',
            'Reason': 'Invoice not found',
            'Remark': 'Invoice with the given PK does not exist',
        }
        return Response(json_data, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("Error --------:", e)
        json_data = {
            'status_code': 500,
            'status': 'Fail',
            'Reason': str(e),
            'Remark': 'Internal Server Error',
        }
        return Response(json_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


