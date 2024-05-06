# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from ..BibliotecaApp.models import User  # Asegúrate de importar tu modelo de usuario aquí

@receiver(post_save, sender=SocialAccount)
def update_password_changed_flag(sender, instance, created, **kwargs):
    if created and instance.provider == 'github':
        instance.user.has_password_changed = True
        instance.user.save()
