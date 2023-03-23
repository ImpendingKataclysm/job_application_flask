import smtplib
import ssl
from dotenv import dotenv_values


def send_email(email, message):
    """
    Sends an email to a given gmail address
    :param email: The email address to send the message to
    :param message: The message body
    :return: None
    """
    # standard host name
    host = "smtp.gmail.com"
    # standard port number
    port = 465

    username = dotenv_values().get("GMAIL_USER")
    password = dotenv_values().get("GMAIL_PASS")

    receiver = email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

