from django.db import connection

def orderValidationandPricing(itemId):
    with connection.cursor() as cursor:
        cursor.execute("SELECT quantity,price FROM main_product WHERE id=%s",[itemId])
        row=cursor.fetchone()
        if row is None:
            return False
        if row[0]>0:
            return [row[0],row[1]] #row[0] denotes quantity and row[1] denotes price
        else:
            return False


