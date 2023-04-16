from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from django.core.mail import send_mail



'''
class Configuration(models.Model):
    email_use_tls = models.BooleanField(_(u'EMAIL_USE_TLS'),default=True)
    email_host = models.CharField(_(u'EMAIL_HOST'),max_length=1024)
    email_host_user = models.CharField(_(u'EMAIL_HOST_USER'),max_length=255)
    email_host_password = models.CharField(_(u'EMAIL_HOST_PASSWORD'),max_length=255)
    email_port = models.PositiveSmallIntegerField(_(u'EMAIL_PORT'),default=587)
    

#config = Configuration.objects.get(**lookup_kwargs)
    
backend = EmailBackend(host=config.host, port=congig.port, username=config.username, 
                       password=config.password, use_tls=config.use_tls, fail_silently=config.fail_silently)

backend = EmailBackend(host="mail.thetrusthospital.com", port="465", username="rex.ampofo@thetrusthospital.com",
                       password="Keep@123$1$", use_tls=True, fail_silently=True)


#EmailBackend(host=None, port=None, username=None, password=None, use_tls=None, fail_silently=False, use_ssl=None, timeout=None, ssl_keyfile=None, ssl_certfile=None)

email = EmailMessage(subject='Test', body='ego be', from_email="rex.ampofo@thetrusthospital.com", to="rex_ohene@yahoo.com",
                     connection=backend)

email.send()


subject = 'welcome to GFG world'
message = f'Hi , thank you for registering in geeksforgeeks.'
email_from = settings.EMAIL_HOST_USER
recipient_list = "rex_ohene@yahoo.com"


print(send_mail( subject, message, email_from, recipient_list ))

'''
# *****(/user/bin/python manage.py)
