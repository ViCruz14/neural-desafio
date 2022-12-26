import base64
from http import HTTPStatus

from fastapi import FastAPI, File, Request, Response, UploadFile, status

from tasks import resize_image

app = FastAPI()

@app.post('/resize')
async def resize(request: Request, file: UploadFile = File(...)):
    if file.content_type:
        payload = await file.read()
        payload_str = base64.b64encode(payload).decode('ascii')

        async_result = resize_image.delay(payload_str).get()
        image_bytes = base64.b64decode(async_result)

        return Response(content=image_bytes, media_type="image")
    else:
        return Response(status_code=HTTPStatus.NO_CONTENT)
