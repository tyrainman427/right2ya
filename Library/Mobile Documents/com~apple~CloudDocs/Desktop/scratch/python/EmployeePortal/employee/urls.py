from django.urls import path
from .views import register,application,event,CalendarView,ApplicantDetailView,EmployeeList, EmployeeDetailView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView,Portal,Announcement,get_form,AnnouncementDetailView

app_name = 'employee'

urlpatterns = [
    path('', Portal.as_view(), name='index'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('event/new/', event, name='event_new'),
    path('event/edit/<str:event_id>', event, name='event_edit'),
    path('applications/', application, name='applicants'),
    path('applications/<int:id>', ApplicantDetailView.as_view(), name='applicant_detail'),
    path('announcements/', Announcement.as_view(), name='announcements'),
    path('announcements/<int:id>/', AnnouncementDetailView.as_view(), name='announcement-details'),
    path('employee/', EmployeeList.as_view(), name='employee-list'),
    path('<int:id>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('new/', EmployeeCreateView.as_view(), name='employee-create'),
    path('add/', get_form, name='announcement-add'),
    path('employee/<pk>/update-employee/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee/<pk>/delete-employee/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('register/', register, name="register"),
]
