import asyncio
from smtplib import SMTP

import numpy as np

from stranger_danger.email.send_mail import Email


def test_connection_check(monkeypatch):
    """Test if connection check works"""

    def connection(*args):
        raise ConnectionError()

    monkeypatch.setattr(Email, "_establish_connection", connection)
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
    _ = asyncio.run(mail.send_email(image))
