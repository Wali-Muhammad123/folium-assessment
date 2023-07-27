# redis_pubsub.py (in both services)
import redis
from django.conf import settings
from celery import Celery

app = Celery('tasks', broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0')

# Create a Redis connection
redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def publish_message_to_redis(instance_id,quantity):
    # Publish the message to a channel
    message_data={
        'instance_id':instance_id,
        'quantity':quantity
    }
    redis_connection.publish('my_channel', message_data)


