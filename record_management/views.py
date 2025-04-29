from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import RecordFile, Record, RecordType, DocumentType, DocumentSubjects, RecordMngExtraFields, RecordExtraFields, Company
from .forms import RecordForm
from django.views import View
from django.http import JsonResponse
import base64
from django.contrib import messages
import datetime as dt
from accounts.models import Profile
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db import transaction
from datetime import datetime


def process_file(request):
    file_data = request.FILES.get('files')
    if file_data:
        file_name = file_data.name
        file_type = file_data.content_type
        file_content = base64.b64encode(file_data.read()).decode('utf-8')
        return file_name, file_type, file_content
    return None

from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_notification_email(record):
    subject = 'Confirmación de Registro'
    from_email = 'felipe.garzon@indepenmedia.co'
    recipient_list = [record.email]

    message = ''
    html_message = render_to_string('email_template.html', {'recordId':record.recordId, 'firstName': record.firstName })

    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

files = []

#@login_required
def index(request, *args, **kwargs):

    flag_filescontrol = False

    # Obtener el usuario logueado y su empresa asociada (si existe)
    user = request.user
    record_extra_fields = None
    if user.id:
        try:
            user_profile = Profile.objects.get(user=user)
            company = user_profile.companyid
        except Profile.DoesNotExist:
            company = None

        # Verificar si el usuario tiene una empresa y si los campos extras están alimentados        
        if company and company.recordextrafields_set.exists():
            record_extra_fields = company.recordextrafields_set.first()
    else:
        # Elegir una empresa por defecto
        company = Company.objects.first()

    if request.method == 'POST':
        form = RecordForm(request.POST, initial={"userOwner": request.user})                
        file_info = process_file(request)
        if file_info:
            file_name, file_type, file_content = file_info
            files.append([file_name, file_type, file_content])
            flag_filescontrol = True
        else:
            flag_filescontrol = False

        if form.is_valid():            
            # Asignar userOwner antes de guardar el registro
            record = form.save(commit=False)  # creamos la instancia sin guardarla

            # Guardar campo company
            if company:
                record.company = company.companyid

            # Guardar campos extra de usuario
            record.extrafield1 = request.POST.get('extrafield1')
            record.extrafield2 = request.POST.get('extrafield2')
            record.extrafield3 = request.POST.get('extrafield3')
            record.extrafield4 = request.POST.get('extrafield4')
            record.extrafield5 = request.POST.get('extrafield5')
            record.extrafield6 = request.POST.get('extrafield6')
            record.extrafield7 = request.POST.get('extrafield7')
            record.extrafield8 = request.POST.get('extrafield8')
            record.extrafield9 = request.POST.get('extrafield9')
            record.extrafield10 = request.POST.get('extrafield10')

            if request.user.is_authenticated:
                record.userOwner = request.user
            else:
                record.userOwner = None

            try:
                with transaction.atomic():
                    record.save()
                    # Realizar las operaciones necesarias con los campos del formulario
                    for file in files:
                        record_file = RecordFile(record=record, namefile=file[0], filetype=file[1], file=file[2])
                        record_file.save()
                    files.clear()

            except IntegrityError:
                messages.error(request, 'Hubo un error al guardar el registro y los archivos adjuntos.')
            else:
                send_notification_email(record)
                # Resto de la lógica de la vista después de la subida de archivos
                messages.success(request, 'El registro se ha guardado correctamente.')

            context = {
                'form': RecordForm(),
                'registro_guardado': True,
                'record_extra_fields': record_extra_fields,  # Pasar los campos extras al contexto
                'company': company,
            }

            messages.get_messages(request).used = True  # Borrar los mensajes

            # Redirigir al formulario vacío
            return render(request, 'record_management_index.html', context)
        else:
            if not flag_filescontrol:
                print(form.errors)
                print(request.POST)

    else:
        # Pasar el usuario logueado al crear una instancia del formulario RecordForm
        if not flag_filescontrol:
            if request.user.is_authenticated:
                form = RecordForm(initial={'firstName': user.first_name, 'lastName':user.last_name, 'email':user.email, 'typeId':user_profile.numberId, 'numberId':user_profile.numberId})
            else:
                form = RecordForm()

    context = {
        'form': form,
        'record_extra_fields': record_extra_fields,  # Pasar los campos extras al contexto
        'company': company,
    }
    return render(request, "record_management_index.html", context)


@login_required
def record_table(request):
    usuario_logueado = request.user
    nombre_usuario = usuario_logueado.username
    email_usuario = usuario_logueado.email

    user = request.user    
    if user.id:
        try:
            user_profile = Profile.objects.get(user=user)
            company = user_profile.companyid
        except Profile.DoesNotExist:
            company = None
    else:
        # Elegir una empresa por defecto
        company = Company.objects.first()

    if request.user.is_staff:
        # No se muestran los registros borrados        
        records = Record.objects.filter(deleted=False).prefetch_related('recordfile_set')
    else:
        records = Record.objects.filter(userOwner=request.user, deleted=False).prefetch_related('recordfile_set')

    context = {
        'usuario': usuario_logueado,
        'nombre_usuario': nombre_usuario,
        'email_usuario': email_usuario,
        'records': records,
        'company': company,
    }

    return render(request, "record_management_table.html", context)

@login_required
def deletedrecord_table(request):
    usuario_logueado = request.user
    nombre_usuario = usuario_logueado.username
    email_usuario = usuario_logueado.email

    user = request.user    
    if user.id:
        try:
            user_profile = Profile.objects.get(user=user)
            company = user_profile.companyid
        except Profile.DoesNotExist:
            company = None
    else:
        # Elegir una empresa por defecto
        company = Company.objects.first()

    if request.user.is_staff:
        # No se muestran los registros borrados        
        records = Record.objects.filter(deleted=True).prefetch_related('recordfile_set')
    else:
        records = Record.objects.filter(userOwner=request.user, deleted=True).prefetch_related('recordfile_set')

    context = {
        'usuario': usuario_logueado,
        'nombre_usuario': nombre_usuario,
        'email_usuario': email_usuario,
        'records': records,
        'company': company,
    }

    return render(request, "deletedrecord_management_table.html", context)

def display_record_search_form(request):
    
    user = request.user    
    if user.id:
        try:
            user_profile = Profile.objects.get(user=user)
            company = user_profile.companyid
        except Profile.DoesNotExist:
            company = None
    else:
        # Elegir una empresa por defecto
        company = Company.objects.first()
    
    context = {
        'company': company,
    }
    return render(request, 'record_search.html', context=context)

def record_search(request):
    if request.method == "POST":
        recordId = request.POST.get('recordId')
        typeId = request.POST.get('typeId')
        numberId = request.POST.get('numberId')
        
        try:
            record = Record.objects.get(recordId=recordId, typeId=typeId, numberId=numberId, deleted=False)
            rec_files = RecordFile.objects.filter(record=record)

            files_data = []        
            for rec_file in rec_files:
                files_data.append({
                    'name': rec_file.namefile,
                    'type': rec_file.filetype,
                    'data': rec_file.file
                })

            # Convertir el objeto de registro a un formato fácilmente representable en JSON para enviarlo de regreso
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio","Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            fecha_formateada = "{} de {} de {}".format(record.recordDate.day, meses[record.recordDate.month - 1], record.recordDate.year)
            
            record_data = {
                'recordId': record.recordId,
                'recordDate': fecha_formateada,
                'firstName': record.firstName,
                'lastName': record.lastName,
                'typeId': record.typeId,
                'numberId': record.numberId,
                'email': record.email,
                'messageType': record.messageType,
                'area': record.area,
                'contractNumber': record.contractNumber,
                'documentDate': record.documentDate,
                'subject': record.subject,
                'url': record.url,
            }
            return JsonResponse({'status': 'success', 'record': record_data, 'files': files_data})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'not_found'})

    return HttpResponseForbidden("Acceso denegado")


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')


# Vista de detalle de registro para Gestor Documental
def record_detail(request, record_id):
    record = get_object_or_404(Record, recordId=record_id, deleted=False)
    rec_files = RecordFile.objects.filter(record=record)
    
    files_data = []        
    for rec_file in rec_files:
        files_data.append({
            'name': rec_file.namefile,
            'type': rec_file.filetype,
            'data': rec_file.file
        })

    try:
        user_profile = Profile.objects.get(user=request.user)
        company_id = user_profile.companyid.id
        record_types = RecordType.objects.filter(companyid=company_id)
        document_types = DocumentType.objects.filter(recordtype__companyid=company_id)
        document_subjects = DocumentSubjects.objects.filter(documenttype__recordtype__companyid=company_id)
        mng_fields = RecordMngExtraFields.objects.filter(companyid=company_id)
        user_fields = RecordExtraFields.objects.filter(companyid=company_id)
    except:
        user_profile = None
        record_types = []
        document_types = []
        document_subjects = []
        mng_fields = []
        user_fields = []    

    if user_profile.is_document_manager:
        template_name = 'record_detail_dc.html'
    else:
        template_name = 'record_detail.html'

    context = {
        'record': record,
        'files': files_data,
        'record_types': record_types,
        'document_types': document_types,
        'document_subjects': document_subjects,
        'mng_fields': mng_fields,
        'user_fields': user_fields,
        'company': user_profile.companyid,
    }
    return render(request, template_name, context)


def obtener_tipos_documentales(request):
    record_type_id = request.GET.get('record_type_id')
    document_types = DocumentType.objects.filter(recordtype_id=record_type_id)
    data = [{'id': doc_type.id, 'description': doc_type.description} for doc_type in document_types]
    return JsonResponse(data, safe=False)

def obtener_tipos_asunto(request):
    document_type_id = request.GET.get('document_type_id')
    document_subjects = DocumentSubjects.objects.filter(documenttype_id=document_type_id)
    data = [{'id': doc_subject.id, 'description': doc_subject.description} for doc_subject in document_subjects]
    return JsonResponse(data, safe=False)


def guardar_registro(request):
    if request.method == 'POST':
        boton_presionado = request.POST.get('action')  # Obtener el botón presionado        
        
        # Obtener datos del formulario
        record_id = request.POST.get('recordId')  # Obtener el recordId del formulario
        record_type_id = request.POST.get('recordType')
        document_type_id = request.POST.get('documentType')
        document_subject_id = request.POST.get('documentSubject')

        # Guardar los datos en tu base de datos
        # Ejemplo de cómo guardar los datos en el modelo Record
        # Obtener el registro existente por su ID
        record = Record.objects.get(pk=record_id)
        # Se presiona boton de borrado, se marca campo de borrado
        if boton_presionado == 'borrar':
            record.deleted = True
        else:
            record.deleted = False
        
        if not record.deleted:
            record.recordType = RecordType.objects.get(pk=record_type_id)
            record.documentType = DocumentType.objects.get(pk=document_type_id)
            record.documentSubject = DocumentSubjects.objects.get(pk=document_subject_id)
        record.filingDate = datetime.now()
        if boton_presionado == 'radicar':
            record.filingNumber = 'Radicado'
        elif boton_presionado == 'rechazar':
            record.filingNumber = 'Rechazado'
                
        record.mngextrafield1 = request.POST.get('mngextrafield1')
        record.mngextrafield2 = request.POST.get('mngextrafield2')
        record.mngextrafield3 = request.POST.get('mngextrafield3')
        record.mngextrafield4 = request.POST.get('mngextrafield4')
        record.mngextrafield5 = request.POST.get('mngextrafield5')
        record.mngextrafield6 = request.POST.get('mngextrafield6')
        record.mngextrafield7 = request.POST.get('mngextrafield7')
        record.mngextrafield8 = request.POST.get('mngextrafield8')
        record.mngextrafield9 = request.POST.get('mngextrafield9')
        record.mngextrafield10 = request.POST.get('mngextrafield10')
        # Configurar otros campos según sea necesario
        try:
            record.save()
        except IntegrityError:
            messages.error(request, 'Hubo un error al guardar el registro.')
        except Exception as e:
            print(str(e))  # Puedes imprimir el mensaje de error para depurar
        else:         
            response_data = {'message': 'Registro guardado exitosamente.',
                             "redirect_url": "/records/"}
            return JsonResponse(response_data, status=200)        
    else:
        # Si la solicitud no es POST, devolver un error
        response_data = {'error': 'Método de solicitud no permitido.'}
        return JsonResponse(response_data, status=405)


def restaurar_registro(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        record_id = request.POST.get('recordId')  # Obtener el recordId del formulario

        # Guardar los datos en tu base de datos
        # Ejemplo de cómo guardar los datos en el modelo Record
        # Obtener el registro existente por su ID
        record = Record.objects.get(pk=record_id)
        record.deleted = False
        record.save()
                
        # Redirigir a la tabla de registros
        response_data = {'message': 'Registro restaurado exitosamente.',
                         "redirect_url": "/deletedrecords/"}
        return JsonResponse(response_data, status=200)    
    else:
        # Si la solicitud no es POST, devolver un error
        response_data = {'error': 'Método de solicitud no permitido.'}
        return JsonResponse(response_data, status=405)