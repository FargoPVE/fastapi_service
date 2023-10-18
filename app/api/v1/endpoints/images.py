import shutil

from fastapi import APIRouter, UploadFile

from app.api.celery_tasks import procces_picture

router = APIRouter(prefix="/images", tags=["Upload images"])


@router.post("/hotels")
async def add_hotel_image(file_name: int, file: UploadFile):
    image_path = f"app/static/images/{file_name}.webp"
    with open(image_path, "+wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
    procces_picture.delay(image_path)
