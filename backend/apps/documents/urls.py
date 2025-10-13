from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'types', views.DocumentTypeViewSet, basename='document-type')
router.register(r'', views.DocumentViewSet, basename='document')

urlpatterns = [
    path('upload/', views.upload_document, name='upload-document'),
    path('batch-upload/', views.batch_upload, name='batch-upload'),
    path('', include(router.urls)),
]

