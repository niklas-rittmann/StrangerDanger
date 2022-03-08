import asyncio
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from typing import Sequence

import cv2
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from stranger_danger.constants.image_types import AnnotadedImage

# Add them for now, move them to database
SENDER = os.getenv("SENDER", "")
PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SERVER = os.getenv("EMAIL_SERVER", "")
PORT = int(os.getenv("EMAIL_PORT", 587))
SUBJECT = os.getenv("EMAIL_SUBJECT", "")


class EmailConstrutor(BaseModel):
    receivers: Sequence[EmailStr]
    sender: str = SENDER
    password: str = PASSWORD
    server: str = SERVER
    port: int = PORT
    subject: str = SUBJECT

    async def send_email(self, image: AnnotadedImage):
        """Send Email to receivers"""
        message = self._create_message(image)
        with SMTP() as smtp:
            smtp = self._establish_connection(smtp)
            emails = [
                self._send_email(message, receiver, smtp) for receiver in self.receivers
            ]
            await asyncio.gather(*emails)

    def check_connection(self) -> bool:
        """Check if the connection to the email server works"""
        with SMTP() as smtp:
            try:
                _ = self._establish_connection(smtp)
            except ConnectionError:
                return False
        return True

    def _create_message(self, image: AnnotadedImage) -> MIMEMultipart:
        """Create multipart message"""
        msg = MIMEMultipart()
        msg["Subject"] = self.subject
        msg["From"] = self.sender
        msg.attach(self._add_image_to_email(image))
        return msg

    def _add_image_to_email(self, image: AnnotadedImage) -> MIMEImage:
        """Attach image to email"""
        return MIMEImage(cv2.imencode(".jpg", image)[1].tostring(), name="Test.jpg")

    def _establish_connection(self, session: SMTP) -> SMTP:
        """Establish a connection to the email server"""
        session.connect(self.server, self.port)
        session.login(self.sender, self.password)
        return session

    async def _send_email(self, message: MIMEMultipart, receiver: str, session: SMTP):
        """Add receiver to message and send"""
        message["To"] = receiver
        session.send_message(message)
