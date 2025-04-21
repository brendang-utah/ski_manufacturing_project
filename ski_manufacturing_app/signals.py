from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Customer

User = get_user_model()

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'customer'):
        Customer.objects.create(user=instance, name=instance.username, email=instance.email)
