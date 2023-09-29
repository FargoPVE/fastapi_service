import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.core.celery import celery_app
from app.core.config import settings
from app.utils.email_templates import create_booking_confirmate_template
from app.utils.logger import logger


@celery_app.task
def procces_picture(path: str):
    im_path = Path(path)
    im = Image.open(im_path)
    for width, height in [
        (1000, 500),
        (200, 100)
    ]:
        resized_img = im.resize(size=(width, height))
        resized_img.save(f"app/static/images/resized_{width}_{height}_{im_path.name}")


@celery_app.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    msg_content = create_booking_confirmate_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
    logger.info(f"Successfully send email message to {email_to}")