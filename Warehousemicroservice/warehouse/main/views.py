from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ViewSet
# Create your views here
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .permissions import IsReadOnlyOrAuthenticated
from .models import Product
from .serializers import ProductSerializer

class ProductAPI(ViewSet):
    serializer_class=ProductSerializer
    permission_classes=[IsReadOnlyOrAuthenticated]
    def create(self,request,*args,**kwargs):
        try:
            super.create(request,*args,**kwargs)
        except ValidationError as e:
            return Response({'error':e.detail},status=status.HTTP_400_BAD_REQUEST)
    def update(self,request,pk=None,*args,**kwargs):
        try:
            super.update(request,pk,*args,**kwargs)
        except ValidationError as e:
            return Response({'error':e.detail},status=status.HTTP_400_BAD_REQUEST)