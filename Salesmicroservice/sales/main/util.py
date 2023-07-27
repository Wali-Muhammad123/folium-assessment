import requests
from django.core.exceptions import ValidationError

def orderValidationandPricing(itemId):
    url=f'http://127.0.0.1:8001/api/product/{itemId}/retrieve_product/'
    response=requests.get(url)
    if response.status_code==200:
        product=response.json()
        if product['product_quantity']>0:
            print(product['product_quantity'],product['product_price'])
            return [product['product_quantity'],product['product_price']]
    else:
        raise ValidationError('Product not found')
    
def updateInventory(itemId,quantity):
    url=f'http://localhost:8001/api/product/{itemId}/update_product_quantity/'
    response=requests.put(url, data={'product_quantity':quantity})
    if response.status_code==200:
        return response.json()
    else:
        raise ValidationError('Product not found')
        


