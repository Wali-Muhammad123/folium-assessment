from django.urls import path, include
from .views import *

urlpatterns = [
    path('orders/',OrderAPI.as_view()),
    path('orders/<int:pk>/',OrderAPI.as_view(),name='order'),
    path('maxorder/',getMaxQuantity,name='maxorder'),
]