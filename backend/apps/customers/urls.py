from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'custom-fields', views.CustomFieldViewSet, basename='custom-field')
router.register(r'', views.CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]

