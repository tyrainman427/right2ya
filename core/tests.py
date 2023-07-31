from django.test import TestCase
from django.core import mail
from core.models import Job, Notification, Customer, User, Meal, Category

class NotificationEmailTestCase(TestCase):
    def setUp(self):
        # Get or create a user
        self.user, _ = User.objects.get_or_create(username='testuser1', defaults={'password': '12345'})

        # Get or create a customer associated with the user
        self.customer, _ = Customer.objects.get_or_create(
            user=self.user, 
            defaults={
                'address': 'Test Address', 
                'phone_number': '1234567890',
                'is_customer': True
            }
        )

        # Get or create a category
        self.category, _ = Category.objects.get_or_create(name='Test Category')

    def tearDown(self):
        if hasattr(self, 'job'):
            Notification.objects.filter(job=self.job).delete()

        self.category.delete()
        self.customer.delete()
        self.user.delete()

    def test_create_job(self):
        # Get or create a job associated with the customer
        self.job, _ = Job.objects.get_or_create(
        customer=self.customer, 
        defaults={
            'name': 'Test Job', 
            'description': 'Test Description', 
            'category': self.category, 
            'size': Job.MEDIUM_SIZE, 
            'quantity': 1, 
            'status': Job.CREATING_STATUS,
            'pickup_address': 'Test Pickup Address',
            'pickup_lat': 0,
            'pickup_lng': 0,
            'pickup_name': 'Test Pickup Name',
            'pickup_phone': '1234567890',
            'delivery_address': 'Test Delivery Address',
            'delivery_lat': 0,
            'delivery_lng': 0,
            'delivery_name': 'Test Delivery Name',
            'delivery_phone': '1234567890',
            'duration': 0,
            'distance': 0,
            'price': 0,
            'service_fee': 0,
            'delivery_fee': 0,
       
            'rated': False
            # Add other required fields here...
            }
        )


        # Check that a notification was created for the job
        notification = Notification.objects.filter(job=self.job).first()
        self.assertIsNotNone(notification, "No notification was created for the job")

        # Check that the notification is associated with the correct user
        self.assertEqual(notification.user, self.user, "The notification is not associated with the correct user")

        # Check that the notification is marked as unread
        self.assertFalse(notification.read, "The notification is marked as read")
