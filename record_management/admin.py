from django.contrib import admin
from .models import RecordExtraFields, RecordMngExtraFields, Record, RecordFile, RecordType, DocumentType, DocumentSubjects

admin.site.register(Record)
#admin.site.register(RecordFile)

@admin.register(RecordType)
class RecordTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'companyid')
    list_filter = ('companyid',)

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'recordtype', 'get_companyid')
    def get_companyid(self, obj):
        return obj.recordtype.companyid
    get_companyid.short_description = 'Company ID' 
    list_filter = ('recordtype__companyid',)

@admin.register(DocumentSubjects)
class DocumentSubjectsAdmin(admin.ModelAdmin):
    list_display = ('documenttype', 'code', 'description', 'get_documenttype_companyid')
    def get_documenttype_companyid(self, obj):
        return obj.documenttype.recordtype.companyid
    get_documenttype_companyid.short_description = 'Company ID'
    list_filter = ('documenttype__recordtype__companyid',)

admin.site.register(RecordExtraFields)
admin.site.register(RecordMngExtraFields)