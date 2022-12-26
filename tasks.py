import base64
import io

from celery import Celery
from celery.contrib import rdb
from PIL import Image

app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672/', backend="redis://redis:6379/0")

@app.task
def resize_image(payload):
    img = Image.open(io.BytesIO(base64.b64decode(payload)))
    new_image = img.resize((384, 384))
    buffer = io.BytesIO()
    new_image.save(buffer, format=img.format)
    image_str = base64.b64encode(buffer.getvalue()).decode('ascii')
    
    return image_str
