from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from .views import UserViewSet, GroupViewSet, RecordApiView, RecordDetailApiView, UpdateRecordApiView
#Rest url
from rest_framework import routers


#Rest
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),    
    path('record/', RecordApiView.as_view(), name='record'),
    path('recorddetail/', RecordDetailApiView.as_view(), name='recordid'),
    path('updaterecord/', UpdateRecordApiView.as_view(), name='updaterecord'),
]