from flask_mail import Mail as _Mail

from flask_mail import Message

from logs.setup_logs import LogSetup

def send_to_email(mail: _Mail, subject, sender, recipients: list, text_msg, html_body = None):
    log = LogSetup(__file__)
    try:
        msg = Message(
            subject=subject,
            sender=sender,
            recipients=recipients,
            body=text_msg,
            html=html_body
        )
        mail.send(msg)
        log.log("info", f"Сообщение отправлено на почту: {recipients}")
    except Exception as e:
        log.log("error", f"Ошибка при отправке сообщения на почту: {e}")