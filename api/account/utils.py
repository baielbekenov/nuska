from django.core.mail import EmailMessage
from django.utils.translation import gettext as _


def send_code_email_confirm(email, code):
    message = EmailMessage(
        to=[email],
        subject=_('Код для подтверждения почты на сайте nuska.kg'),
        body=_(f'Ваш код для подтверждения {code}.\nНикому не говорите ваш код'),
    )

    message.send()
    return True