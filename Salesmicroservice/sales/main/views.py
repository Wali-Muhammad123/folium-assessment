from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from queries.ordervalidation import orderValidationandPricing
from .models import Order
from .serializers import OrderSerializer

class OrderAPI(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=OrderSerializer
    def get(self,request):
        orders=Order.objects.all()
        serializer=self.serializer_class(orders,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except: 
                return Response({'error':'Insufficient Quantity available'},status=400)
            return Response(serializer.data)
        return Response(serializer.errors)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def getMaxQuantity(request):
    maxQuantity=orderValidationandPricing(itemId=request.data['itemId'])
    if maxQuantity:
        serializer=OrderSerializer(data={'name':request.data['itemId'],'quantity':maxQuantity[0]})
        if serializer.is_valid():
            return Response({'maxQuantity':maxQuantity[0],'msg':"Max Quantity of the related item purchased successfully"},status=200)
        else:
            return Response({'error':serializer.errors},status=400)
    else:
        return Response({'error':"Item doesn't exist"},status=400)
