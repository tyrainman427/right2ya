from django.contrib import admin
from .models import Announcement, Employee, Event
import datetime
import calendar
from django.urls import reverse
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ['day', 'start_time', 'end_time', 'notes']


admin.site.register(Event)
admin.site.register(Announcement)
admin.site.register(Employee)
