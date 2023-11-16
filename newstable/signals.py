from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.core.signing import Signer, loads, dumps
from django.core.mail import EmailMessage
from prac import settings


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.is_active = False
        instance.save()
        user_email = instance.email
        token = dumps(user_email)
        signer = Signer()
        signed_token = signer.sign(token)
        email = EmailMessage(subject='Confirmation', body=f'http://127.0.0.1:8000/confirm-email/{signed_token}', to=[user_email])
        email.send()
