import asyncio
from os import wait
from smtplib import SMTP

import numpy as np

from stranger_danger.email import send_mail
from stranger_danger.email.send_mail import Email


def test_connection_check(monkeypatch):
    """Test if connection check works"""
    assert not Email(server="", receivers=["test@tests.de"]).check_connection()

    monkeypatch.setattr(Email, "_establish_connection", lambda x, y: True)
    assert Email(server="", receivers=["test@tests.de"]).check_connection()


def test_create_message():
    """Test if message gets formatted the right way"""
    rec, sender, sub = (
        ["test@test.de"],
        "me",
        "test",
    )

    mail = Email(receivers=rec, sender=sender, subject=sub)
    image = (np.random.rand(255, 255, 3) * 255).astype(np.uint8)
    message = mail._create_message(image)
    assert message["From"] == sender
    assert message["Subject"] == sub


def test_send_message(monkeypatch):
    """Test if message gets formatted the right way"""
    rec, sender, sub = (
        ["test@test.de"],
        "me",
        "test",
    )

    class Session:
        def send_message(*args, **kwargs):
            return

    monkeypatch.setattr(Email, "_establish_connection", lambda x, y: Session)
    monkeypatch.setattr(SMTP, "send_message", lambda x: True)
    mail = Email(receivers=rec, sender=sender, subject=sub)
    image = (np.random.rand(255, 255, 3) * 255).astype(np.uint8)
    message = asyncio.run(mail.send_email(image))


"""
class Email(BaseModel):
    receivers: Sequence[EmailStr]
    sender: str = SENDER
    password: str = PASSWORD
    server: str = SERVER
    port: int = PORT
    subject: str = SUBJECT

    async def send_email(self, image: Image):
        ""Send Email to receivers""
        message = self._create_message(image)
        with SMTP() as smtp:
            smtp = self._establish_connection(smtp)
            emails = [
                self._send_email(message, receiver, smtp) for receiver in self.receivers
            ]
            await asyncio.gather(*emails)

    def check_connection(self) -> bool:
        ""Check if the connection to the email server works""
        with SMTP() as smtp:
            try:
                _ = self._establish_connection(smtp)
            except ConnectionError:
                return False
        return True

    def _create_message(self, image: Image) -> MIMEMultipart:
        ""Create multipart message""
        msg = MIMEMultipart()
        msg["Subject"] = self.subject
        msg["From"] = self.sender
        msg.attach(self._add_image_to_email(image))
        return msg

    def _add_image_to_email(self, image: Image) -> MIMEImage:
        ""Attach image to email""
        return MIMEImage(image.tobytes(), _subtype="jpg")

    def _establish_connection(self, session: SMTP) -> SMTP:
        ""Establish a connection to the email server""
        session.connect(self.server, self.port)
        session.login(self.sender, self.password)
        return session

    async def _send_email(self, message: MIMEMultipart, receiver: str, session: SMTP):
        ""Add receiver to message and send""
        message["To"] = receiver
        session.send_message(message)"""
