from django.db import models
#import uuid field
from uuid import uuid4
#import min value validator
from django.core.validators import MinValueValidator
# Create your models here.
class Product(models.Model):
    product_id=models.UUIDField(primary_key=True,default=uuid4,editable=False)
    product_name=models.CharField(max_length=100)
    product_price=models.IntegerField(validators=[MinValueValidator(0)])
    product_quantity=models.IntegerField(validators=[MinValueValidator(0)])
    product_description=models.TextField(max_length=500,default="No description available")
    class Meta:
        db_table='warehouse_item'



