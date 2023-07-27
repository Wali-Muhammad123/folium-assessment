from django.db import models
#import minvaluevalidator
from django.core.validators import MinValueValidator
from queries.ordervalidation import orderValidationandPricing
# Create your models here.
class Order(models.Model):
    name=models.CharField(max_length=100)
    quantity=models.IntegerField(validators=[MinValueValidator(1)])
    price=models.IntegerField()
    class Meta:
        db_table='sales_orders'
    def save(self,*args,**kwargs):
        validOrder=orderValidationandPricing(itemId=self.name)
        if validOrder:
            if validOrder[0]>=self.quantity:
                self.price=validOrder[1]*self.quantity
                super(Order,self).save(*args,**kwargs)
            else:
                raise Exception("Insufficient Quanity available")
