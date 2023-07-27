import redis
from django.conf import settings
from celery import Celery
from main.models import Product

app = Celery('tasks', broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0')

# Create a Redis connection
redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def subscribe_to_redis_channel():
    # Subscribe to the channel and process the received messages
    pubsub = redis_connection.pubsub()
    pubsub.subscribe('my_channel')

    for message in pubsub.listen():
        if message['type'] == 'message':
            # Call the Celery task to update the database in Service 1
            update_database.delay(message['data'])  # Use the Celery task

@app.task
def update_database(message_data):
    instance_id=message_data.get('instance_id')
    product_quantity=message_data.get('product_quantity')
    try:
        product=Product.objects.get(instance_id=instance_id)
        product.product_quantity=product_quantity
        product.save()
        return "Database updated successfully."
    except Product.DoesNotExist:
        return "Product not found."
    