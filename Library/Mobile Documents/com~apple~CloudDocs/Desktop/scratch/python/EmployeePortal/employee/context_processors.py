def announcements(request):
    from employee.models import Announcement
    return {'announcements': Announcement.objects.all()
    }

def employees(request):
    from employee.models import Employee
    return {'employee': Employee.objects.filter(is_active=False)
    }
