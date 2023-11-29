from django.core.mail import EmailMessage


def send_email_code(email, code):
    message = EmailMessage(
        to=[email],
        subject='nuska.kg сайтында каттоо коду',
        body=f'Каттоо кодуңуз — {code}.\nКодуңузду эч кимге айтпаңыз',
    )

    message.send()
    return True


def send_email_code_for_reset(email, code):
    message = EmailMessage(
        to=[email],
        subject='nuska.kg сайтында кодду калыбына келтирүү',
        body=f'Баштапкы абалга келтирүү кодуңуз — {code}.\nКодуңузду эч кимге айтпаңыз',
    )

    message.send()
    return True