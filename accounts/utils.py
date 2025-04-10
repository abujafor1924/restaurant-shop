from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings


def detectUserType(user):
     if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
     elif user.role == 2:
        redirectUrl = 'customerDashboard'
        return redirectUrl
     elif user.role == None and user.is_superadmin == True: 
        redirectUrl = '/admin'
        return redirectUrl
     
     
   
     
     
def  send_email_for_verification(request,user, mail_subject,email_template):
     default_from_email=settings.DEFAULT_FROM_EMAIL
     current_site = get_current_site(request)
     mail_subject = 'Please activate your account'
     message = render_to_string(email_template, {
        "user": user,
        'domain': current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
     })
     to_email = user.email
     send_email = EmailMessage(mail_subject, message, default_from_email, to=[to_email])
     send_email.send()  
     


def send_test_email():
    try:
        send_mail(
            'Test Email Subject',
            'This is a test email body.',
            'django.soyad.abu.jafor@gmail.com',  # From email
            ['soyad.abu.jafor@gmail.com'],  # To email
            fail_silently=False,
        )
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


# def send_email_for_reset_password(request,user,uidb64,token):
#      default_from_email=settings.DEFAULT_FROM_EMAIL
#      current_site = get_current_site(request)
#      mail_subject = 'Reset your password'
#      message = render_to_string('accounts/email/reset_password_email.html', {
#         "user": user,
#         'domain': current_site.domain,
#         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': default_token_generator.make_token(user),
#      })
#      to_email = user.email
#      send_email = EmailMessage(mail_subject, message, default_from_email, to=[to_email])
#      send_email.send()




def send_notification(mail_subject,mail_template,context):
     default_from_email=settings.DEFAULT_FROM_EMAIL
     message = render_to_string(mail_template, context)
     to_email = context['user'].email
     send_email = EmailMessage(mail_subject, message, default_from_email, to=[to_email])
     send_email.send()