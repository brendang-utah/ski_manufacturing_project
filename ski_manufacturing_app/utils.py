from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_status_email(order):
    """Send email notification about order status change."""
    subject = f'Order #{order.id} Status Update'
    context = {
        'order': order,
        'customer_name': order.customer.user.username,
        'status': order.get_status_display(),
    }
    
    html_message = render_to_string('ski_manufacturing_app/email/order_status_update.html', context)
    plain_message = render_to_string('ski_manufacturing_app/email/order_status_update.txt', context)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.customer.user.email],
        html_message=html_message
    )