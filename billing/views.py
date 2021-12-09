from django.conf import settings
from django.core.mail import EmailMessage
from django.http.response import HttpResponse

def send_email(response):
    subject = 'receipt',
    body = 'bodyyy',
    email = 'admin@empowerthevillage.org'
    try:
        print('tried')
        email_msg = EmailMessage(
            subject=subject, 
            body = body, 
            from_email='admin@empowerthevillage.org', 
            to=['chandlerprevatt@utexas.edu'], 
            reply_to=[email]
            )
        print(email_msg)
        email_msg.send()
        return HttpResponse('sent!')
    except:
        return "Message failed, try again later :("