import random
import string
from django.contrib import admin, messages
from django.conf import settings
from paypalrestsdk import configure, Payout
from decimal import Decimal


from .models import *


configure({
  "mode": settings.PAYPAL_MODE,
  "client_id": settings.PAYPAL_CLIENT_ID,
  "client_secret": settings.PAYPAL_CLIENT_SECRET,
})


def payout_to_courier(modeladmin, request, queryset):
    payout_items = []
    transaction_querysets = []

    # Step 1 - Get all the valid couriers in queryset
    for courier in queryset:
        if courier.paypal_email:
            # Separate transactions for job and tip
            job_transactions = Transaction.objects.filter(
                job__courier=courier,
                status=Transaction.IN_STATUS,
                transaction_type=Transaction.JOB
            )

            tip_transactions = Transaction.objects.filter(
                job__courier=courier,
                status=Transaction.IN_STATUS,
                transaction_type=Transaction.TIP
            )

            # Sum up the job amounts (80% of each job amount)
            job_balance = sum(Decimal(str(t.amount)) * Decimal("0.8") for t in job_transactions)

            print("job balance:", job_balance)

            # Sum up the tip amounts (100% of each tip)
            tip_balance = sum(t.amount for t in tip_transactions)
            print("Tip: ", tip_balance)
            
            # Calculate the total balance
            total_balance = Decimal(job_balance) + Decimal(tip_balance)

            print("Total balance:", total_balance)

            if total_balance > 0:
                payout_items.append({
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": "{:.2f}".format(total_balance),
                        "currency": "USD"
                    },
                    "receiver": courier.paypal_email,
                    "note": "Thank you.",
                    "sender_item_id": str(courier.id)
                })

                transaction_querysets.append(job_transactions | tip_transactions)  # Union of both querysets
            # Inside the loop for each courier in payout_to_courier
    print(f"Debugging for courier: {courier.id}")
    print(f"Job Transactions: {job_transactions.values('id', 'amount')}")
    print(f"Tip Transactions: {tip_transactions.values('id', 'amount')}")
    print(f"Job Balance: {job_balance}")
    print(f"Tip Balance: {tip_balance}")
    print(f"Total Balance: {total_balance}")

    # Step 2 - Send payout batch + email to receivers
    sender_batch_id = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": sender_batch_id,
            "email_subject": "You have a payment"
        },
        "items": payout_items
    })

    # Step 3 - Execute Payout process and Update transactions' status to "OUT" if successful
    try:
        if payout.create():
            for t in transaction_querysets:
                t.update(status=Transaction.OUT_STATUS)
            messages.success(request, "payout[%s] created successfully" % (payout.batch_header.payout_batch_id))
        else:
            messages.error(request, payout.error)
    except Exception as e:
        messages.error(request, str(e))

payout_to_courier.short_description = "Payout to Couriers"


class CourierAdmin(admin.ModelAdmin):
  list_display = ['user_full_name', 'paypal_email', 'balance']
  actions = [payout_to_courier]

  def user_full_name(self, obj):
    return obj.user.get_full_name()


  def balance(self, obj):
    job_transactions = Transaction.objects.filter(
        job__courier=obj, 
        status=Transaction.IN_STATUS, 
        transaction_type=Transaction.JOB
    )
    
    tip_transactions = Transaction.objects.filter(
        job__courier=obj, 
        status=Transaction.IN_STATUS, 
        transaction_type=Transaction.TIP
    )

    print(f"Job Transactions: {job_transactions.values('id', 'amount')}")  # Debug
    print(f"Tip Transactions: {tip_transactions.values('id', 'amount')}")  # Debug
    
    # Sum up 80% of the job amounts
    job_balance = sum(Decimal(t.amount) * Decimal("0.8") for t in job_transactions)
    print(f"Job Balance: {job_balance}")  # Debug

    # Sum up the tip amounts (100% goes to the courier)
    tip_balance = sum(Decimal(t.amount) for t in tip_transactions)
    print(f"Tip Balance: {tip_balance}")  # Debug
    
    # Calculate the total balance
    total_balance = job_balance + tip_balance
    print(f"Total Balance: {total_balance}")  # Debug
    
    return round(total_balance, 2)



class TransactionAdmin(admin.ModelAdmin):
  list_display = ['stripe_payment_intent_id', 'courier_paypal_email', 'customer', 'courier', 'job', 'amount', 'status', 'created_at']
  list_filter = ['status',]

  def customer(self, obj):
    return obj.job.customer

  def courier(self, obj):
    return obj.job.courier

  def courier_paypal_email(self, obj):
    return obj.job.courier.paypal_email if obj.job.courier else None

# Register your models here.
admin.site.register(Customer)
admin.site.register(Courier, CourierAdmin)
admin.site.register(Category)
admin.site.register(Job)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Restaurant)
admin.site.register(Meal)
admin.site.register(Rating)
admin.site.register(Notification)
admin.site.register(Tip)