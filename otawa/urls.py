"""
URL configuration for otawa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from record_management import views as rmviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', rmviews.index, name='Record Management'),
    path('records/', rmviews.record_table, name='record_table'),
    path('deletedrecords/', rmviews.deletedrecord_table, name='deletedrecord_table'),
    path('record_search/', rmviews.record_search, name='record_search'),
    path('buscar_registro/', rmviews.display_record_search_form, name='display_record_search_form'),
    path('record_detail/<int:record_id>/', rmviews.record_detail, name='record_detail'),
    path('api/', include('api.urls')),
    #path('new_record/', rmviews.new_record, name='new_record'),
    #path('create_record/', rmviews.create_record, name='create_record'),
    #path('add_user_profile/', rmviews.add_user_profile, name='add_user_profile'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('terms-and-conditions', rmviews.terms_and_conditions, name='terms_and_conditions' ),
    # URLS para vista de GD
    path('obtener_tipos_documentales/', rmviews.obtener_tipos_documentales, name='obtener_tipos_documentales'),
    path('obtener_tipos_asunto/', rmviews.obtener_tipos_asunto, name='obtener_tipos_asunto'),
    path('guardar_registro/', rmviews.guardar_registro, name='guardar_registro'),
    path('restaurar_registro/', rmviews.restaurar_registro, name='restaurar_registro'),    
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)