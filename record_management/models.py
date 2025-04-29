from django.db import models
from django.contrib.auth.models import User
from accounts.models import Company

# Create your models here.
class Record(models.Model):
    recordId    = models.AutoField(primary_key=True, verbose_name='Número de radicado')    
    recordDate  = models.DateTimeField(auto_now=True)
    filingNumber = models.CharField(max_length=30, verbose_name='Número de radicado', null=True, blank=True)
    filingDate  = models.DateField(verbose_name='Fecha de radicado', null=True, blank=True)
    userOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records', null=True, blank=True)
    typeId      = models.CharField(max_length=4, verbose_name='Tipo de identificación')
    numberId    = models.CharField(max_length=30, verbose_name='Número de identificación')
    firstName   = models.CharField(max_length=100, verbose_name='Nombres')
    lastName    = models.CharField(max_length=100, verbose_name='Apellido', null=True, blank=True)
    email       = models.EmailField(verbose_name='Correo electrónico')
    contactperson = models.CharField(max_length=150, verbose_name='Persona de contacto', blank=True, null=True)
    messageType = models.CharField(max_length=50, verbose_name='Tipo de mensaje')
    area        = models.CharField(max_length=50, verbose_name='Área de recepción')
    contractNumber  = models.CharField(max_length=30, verbose_name='Número de contrato', blank=True, null=True)
    documentDate    = models.DateField(verbose_name='Fecha del documento')
    subject = models.CharField(max_length=250, verbose_name='Asunto', blank=True, null=True)
    url         = models.URLField(max_length=300, verbose_name="Link", blank=True, null=True)
    replyCheck  = models.BooleanField(verbose_name='Respuesta requerida')
    # Company
    companyid = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Empresa')
    # DM Fields
    recordType = models.ForeignKey('RecordType', on_delete=models.CASCADE, verbose_name='Tipo de correspondencia', null=True, blank=True)
    documentType = models.ForeignKey('DocumentType', on_delete=models.CASCADE, verbose_name='Tipo documental', null=True, blank=True)
    documentSubject = models.ForeignKey('DocumentSubjects', on_delete=models.CASCADE, verbose_name='Tipo de asunto', null=True, blank=True)
    # Extra Fields
    extrafield1 = models.CharField(max_length=100, verbose_name='Campo adicional 1', null=True, blank=True)
    extrafield2 = models.CharField(max_length=100, verbose_name='Campo adicional 2', null=True, blank=True)
    extrafield3 = models.CharField(max_length=100, verbose_name='Campo adicional 3', null=True, blank=True)
    extrafield4 = models.CharField(max_length=100, verbose_name='Campo adicional 4', null=True, blank=True)
    extrafield5 = models.CharField(max_length=100, verbose_name='Campo adicional 5', null=True, blank=True)
    extrafield6 = models.CharField(max_length=100, verbose_name='Campo adicional 6', null=True, blank=True)
    extrafield7 = models.CharField(max_length=100, verbose_name='Campo adicional 7', null=True, blank=True)
    extrafield8 = models.CharField(max_length=100, verbose_name='Campo adicional 8', null=True, blank=True)
    extrafield9 = models.CharField(max_length=100, verbose_name='Campo adicional 9', null=True, blank=True)
    extrafield10 = models.CharField(max_length=100, verbose_name='Campo adicional 10', null=True, blank=True)
    # MNG Fields
    mngextrafield1 = models.CharField(max_length=100, verbose_name='Campo adicional mng 1', null=True, blank=True)
    mngextrafield2 = models.CharField(max_length=100, verbose_name='Campo adicional mng 2', null=True, blank=True)
    mngextrafield3 = models.CharField(max_length=100, verbose_name='Campo adicional mng 3', null=True, blank=True)
    mngextrafield4 = models.CharField(max_length=100, verbose_name='Campo adicional mng 4', null=True, blank=True)
    mngextrafield5 = models.CharField(max_length=100, verbose_name='Campo adicional mng 5', null=True, blank=True)
    mngextrafield6 = models.CharField(max_length=100, verbose_name='Campo adicional mng 6', null=True, blank=True)
    mngextrafield7 = models.CharField(max_length=100, verbose_name='Campo adicional mng 7', null=True, blank=True)
    mngextrafield8 = models.CharField(max_length=100, verbose_name='Campo adicional mng 8', null=True, blank=True)
    mngextrafield9 = models.CharField(max_length=100, verbose_name='Campo adicional mng 9', null=True, blank=True)
    mngextrafield10 = models.CharField(max_length=100, verbose_name='Campo adicional mng 10', null=True, blank=True)
    # Deleted indicator
    deleted = models.BooleanField(default=False, verbose_name='Eliminado')

    class Meta:
        db_table = 'mvnt_record'
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

    def __str__(self):
        return str(self.recordId)


class RecordFile(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    namefile = models.CharField(max_length=255, verbose_name='Nombre de archivo')
    filetype = models.CharField(max_length=100, verbose_name='Tipo de archivo')
    file = models.TextField()

    class Meta:
        db_table = 'mvnt_recordfile'
        verbose_name = 'Archivo de registro'
        verbose_name_plural = 'Archivos de registro'

    def __str__(self):
        return self.namefile


class RecordExtraFields(models.Model):
    companyid = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Empresa')
    extrafield1 = models.CharField(max_length=100, verbose_name='Campo adicional 1', null=True, blank=True)
    extrafield2 = models.CharField(max_length=100, verbose_name='Campo adicional 2', null=True, blank=True)
    extrafield3 = models.CharField(max_length=100, verbose_name='Campo adicional 3', null=True, blank=True)
    extrafield4 = models.CharField(max_length=100, verbose_name='Campo adicional 4', null=True, blank=True)
    extrafield5 = models.CharField(max_length=100, verbose_name='Campo adicional 5', null=True, blank=True)
    extrafield6 = models.CharField(max_length=100, verbose_name='Campo adicional 6', null=True, blank=True)
    extrafield7 = models.CharField(max_length=100, verbose_name='Campo adicional 7', null=True, blank=True)
    extrafield8 = models.CharField(max_length=100, verbose_name='Campo adicional 8', null=True, blank=True)
    extrafield9 = models.CharField(max_length=100, verbose_name='Campo adicional 9', null=True, blank=True)
    extrafield10 = models.CharField(max_length=100, verbose_name='Campo adicional 10', null=True, blank=True)

    class Meta:
        db_table = 'mvnt_recordextrafields'
        verbose_name = 'Formulario - campo adicional'
        verbose_name_plural = 'Formulario - campos adicionales'

    def __str__(self):
        return self.companyid.companyname


class RecordMngExtraFields(models.Model):
    companyid = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Empresa')
    extrafield1 = models.CharField(max_length=100, verbose_name='Campo adicional 1', null=True, blank=True)
    extrafield2 = models.CharField(max_length=100, verbose_name='Campo adicional 2', null=True, blank=True)
    extrafield3 = models.CharField(max_length=100, verbose_name='Campo adicional 3', null=True, blank=True)
    extrafield4 = models.CharField(max_length=100, verbose_name='Campo adicional 4', null=True, blank=True)
    extrafield5 = models.CharField(max_length=100, verbose_name='Campo adicional 5', null=True, blank=True)
    extrafield6 = models.CharField(max_length=100, verbose_name='Campo adicional 6', null=True, blank=True)
    extrafield7 = models.CharField(max_length=100, verbose_name='Campo adicional 7', null=True, blank=True)
    extrafield8 = models.CharField(max_length=100, verbose_name='Campo adicional 8', null=True, blank=True)
    extrafield9 = models.CharField(max_length=100, verbose_name='Campo adicional 9', null=True, blank=True)
    extrafield10 = models.CharField(max_length=100, verbose_name='Campo adicional 10', null=True, blank=True)

    class Meta:
        db_table = 'mvnt_recordmngextrafields'
        verbose_name = 'Gestor Documental - campo adicional'
        verbose_name_plural = 'Gestor Documental -  campos adicionales'

    def __str__(self):
        return self.companyid.companyname


class RecordType(models.Model):
    companyid = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Empresa')
    code = models.CharField(max_length=4, verbose_name='Código Tipo de correspondencia')
    description = models.CharField(max_length=100, verbose_name='Descripción de Tipo de correspondencia')

    class Meta:    
        verbose_name = 'Tipo de correspondencia'
        verbose_name_plural = 'Tipos de correspondencia'

    def __str__(self):
        return f"{self.pk}"


class DocumentType(models.Model):
    recordtype = models.ForeignKey(RecordType, on_delete=models.CASCADE, verbose_name='Tipo de correspondencia')
    code = models.CharField(max_length=4, verbose_name='Código Tipo de documento')
    description = models.CharField(max_length=100, verbose_name='Descripción de Tipo de documento')

    class Meta:    
        verbose_name = 'Tipo documental'
        verbose_name_plural = 'Tipos documentales'
        

    def __str__(self):
        return f"{self.pk}"


class DocumentSubjects(models.Model):
    documenttype = models.ForeignKey(DocumentType, on_delete=models.CASCADE, verbose_name='Tipo de documento')
    code = models.CharField(max_length=4, verbose_name='Código de asunto')
    description = models.CharField(max_length=100, verbose_name='Descripción de asunto')

    class Meta:    
        verbose_name = 'Tipo de asunto'
        verbose_name_plural = 'Tipos de asuntos'

    def __str__(self):
        return f"{self.pk}"