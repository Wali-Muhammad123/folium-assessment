from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductAPI

router=DefaultRouter()
router.register('product',ProductAPI,basename='product')

urlpatterns=[
    path('',include(router.urls))
]