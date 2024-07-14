from django.contrib import admin
from .models import Contact, Property, PropertyImage, Service, Appointment, Invoice, Document

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('address', 'contact')
    list_filter = ('address',)
    search_fields = ('address',)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'contact', 'date_of_service', 'total')
    list_filter = ('date_of_service',)
    search_fields = ('invoice_number', 'contact__name')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('service', 'date', 'property')
    list_filter = ('date', 'service')
    search_fields = ('property__address', 'service__name')

admin.site.register(Contact, ContactAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(PropertyImage)
admin.site.register(Service)
admin.site.register(Document)
