from django.contrib import admin
from .models import WorkOrder

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'contact', 'property', 'verify_address', 'evaluate_driveway', 'cover_condition', 'fluid_level']
    # You can add more options like list_filter, search_fields, etc., as needed.
