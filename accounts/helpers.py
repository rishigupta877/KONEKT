


from django.core.mail import send_mail

from django.conf import settings 


def send_forget_password_mail(user , token ):
    subject = 'Your forget password link'
    message = f'Hi {user.username}, click on the link to reset your password http://127.0.0.1:8000/accounts/password_reset_confirm/{token}/'
    
    recipient_list = [user.email]
    send_mail(subject, message, '', recipient_list)
    return True
