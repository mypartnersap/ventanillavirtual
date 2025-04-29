from pydoc import Doc
from re import I
from django.shortcuts import render
#Rest
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer
# Rest Upload files
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status
from record_management.models import Record, RecordFile, RecordType, DocumentType, DocumentSubjects
import os
import base64
#import magic
from datetime import datetime

# Imports WS SOAP
#from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken
import logging
import json
from rest_framework import serializers

from django.template.loader import render_to_string
from django.core.mail import send_mail


#Notificaciones
def filingnumber_notification(record):
    subject = 'Confirmación de Radicado'
    from_email = 'felipe.garzon@indepenmedia.co'
    recipient_list = [record.email]

    message = ''
    html_message = render_to_string('filingnumber_updatemessage.html', {'radicado':record.filingNumber })

    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

#Rest Views
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'

class RecordFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordFile
        fields = '__all__'


class RecordTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordType
        fields = ('code', 'description')

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('code', 'description')

class DocumentSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSubjects
        fields = ('code', 'description')

class RecordApiView(APIView):
    def get(self, request, format=None):                
        date = request.query_params.get('date')        
        # Example: http://127.0.0.1:8000/api/record/?date=2023-09-14        
        try:
            logging.basicConfig(level=logging.DEBUG)
            # Consulta los Record por fecha y devuelve un JSON con los registros
            date_qr = datetime.strptime(date, '%Y-%m-%d').date()
            records = Record.objects.filter(recordDate__year=date_qr.year, recordDate__month=date_qr.month, recordDate__day=date_qr.day, deleted=False)
            records_json = records.values()
        except Exception as e:
            return Response(data='Error en la consulta: ' + str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=records_json, status=status.HTTP_200_OK)

class RecordDetailApiView(APIView):
    def get(self, request, format=None):                
        recordid = request.query_params.get('id')       
        # Example: http://127.0.0.1:8000/api/recorddetail/?id=13         
        try:
            logging.basicConfig(level=logging.DEBUG)
            # Consulta los Record por fecha y devuelve un JSON con los registros
            record = Record.objects.select_related('recordType', 'documentType', 'documentSubject').get(recordId=recordid, deleted=False)
            recordfiles = RecordFile.objects.filter(record_id=recordid)

            # Serializa los datos de registros y archivos
            records_serializer = RecordSerializer(record)
            recordfiles_serializer = RecordFileSerializer(recordfiles, many=True)

            # Serializa los campos RecordType, DocumentType y DocumentSubjects correctamente
            record_type_serializer = RecordTypeSerializer(record.recordType)
            document_type_serializer = DocumentTypeSerializer(record.documentType)
            document_subjects_serializer = DocumentSubjectsSerializer(record.documentSubject)

            # Crea un diccionario que contenga ambas serializaciones
            response_data = {
                'records': records_serializer.data,
                'recordfiles': recordfiles_serializer.data,
                'recordType': record_type_serializer.data,
                'documentType': document_type_serializer.data,
                'documentSubject': document_subjects_serializer.data
            }

            return Response(data=response_data, status=status.HTTP_200_OK)

        except Record.DoesNotExist:
            return Response(data='Registro no encontrado', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data='Error en la consulta: ' + str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UpdateRecordApiView(APIView):
    # Given jason data with record_id, filingNumber and filingDate, update record model
    def post(self, request, format=None):                     
        #Example url http://127.0.0.1:8000/api/updaterecord/
        #Example json {"record_id": 13, "filingNumber": "123456", "filingDate": "2021-09-14"}
        try:
            logging.basicConfig(level=logging.DEBUG)
            # Consulta los Record por fecha y devuelve un JSON con los registros
            record_id = request.data['record_id']
            filingNumber = request.data['filingNumber']
            filingDate = request.data['filingDate']
            record = Record.objects.get(recordId=record_id)
            record.filingNumber = filingNumber
            record.filingDate = filingDate
            record.save()            
            # Envía correo de notificación
            filingnumber_notification(record=record)
                        
        except Exception as e:
            return Response(data='Error en la consulta: ' + str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data='Registro actualizado', status=status.HTTP_200_OK)
        