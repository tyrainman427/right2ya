from django.contrib import admin
from .models import Email

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent_date', 'delivery_status', 'times_sent')
    list_filter = ('sent_date', 'delivery_status')
    search_fields = ('contact__name', 'property__address', 'subject')

    # Optionally, add more customization as needed
