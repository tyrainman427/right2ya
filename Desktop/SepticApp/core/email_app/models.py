from django.db import models
from contacts.models import Invoice, Contact

class Email(models.Model):
    EMAIL_TYPES = [
        ('invoice', 'Invoice'),
        ('estimate', 'Estimate'),
        ('receipt', 'Receipt'),
    ]

    email_type = models.CharField(max_length=10, choices=EMAIL_TYPES, default='invoice')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='emails', null=True, blank=True)

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='emails', null=True, blank=True)
    #estimate = models.ForeignKey(Estimate', on_delete=models.CASCADE, related_name='emails', null=True, blank=True)
    #receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE, related_name='emails', null=True, blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=100, default='Not Sent')
    times_sent = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_email_type_display()} Email - {self.subject}"
