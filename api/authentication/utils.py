from django.core.mail import EmailMessage


def send_email_code(email, code):
    message = EmailMessage(
        to=[email],
        subject='Код для регистрации на сайте nuska.kg',
        body=f'Ваш код для регистрации {code}.\nНикому не говорите ваш код',
    )

    message.send()
    return True


def send_email_code_for_reset(email, code):
    message = EmailMessage(
        to=[email],
        subject='Код для сброса на сайте nuska.kg',
        body=f'Ваш код для сброса {code}.\nНикому не говорите ваш код',
    )

    message.send()
    return True