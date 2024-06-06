#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""email"""

import os
import smtplib
from email.mime.text import MIMEText


def sendmail(to: str, subject: str, content: str) -> None:
    """send mail to an address"""

    msg: MIMEText = MIMEText(content)

    msg["Subject"] = f"[Ari-web] {subject}"
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = to

    server: smtplib.SMTP = smtplib.SMTP(os.environ["EMAIL_SERVER"], 587)

    server.ehlo()
    server.starttls()

    server.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASSWORD"])

    server.send_message(msg)
    server.quit()
