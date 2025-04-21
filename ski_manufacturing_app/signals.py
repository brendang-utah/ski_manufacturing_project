from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Customer, Employee

User = get_user_model()

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    # Only create customer profile if:
    # 1. This is a newly created user
    # 2. The user doesn't already have a customer profile
    # 3. The user isn't an employee
    if created and not hasattr(instance, 'customer') and not hasattr(instance, 'employee'):
        Customer.objects.create(user=instance)
