import os
import django

# Set the environment variable to point to your Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from contacts.models import Service

# Data to be added to the Service model
services_data = [
    {"name": "Additional Man Labor per hour", "price": 105.00, "quantity": 1},
    {"name": "Boost - 1000gal Combo", "price": 209.99, "quantity": 1},
    {"name": "Boost - 1250gal Combo", "price": 249.99, "quantity": 1},
    {"name": "Boost - 1500gal Combo", "price": 249.99, "quantity": 1},
    {"name": "Boost 1 Unit", "price": 54.99, "quantity": 1},
    {"name": "Boost 2 Units", "price": 109.99, "quantity": 1},
    {"name": "Boost 3 Units", "price": 164.99, "quantity": 1},
    {"name": "Boost Additional Units", "price": 54.99, "quantity": 1},
    {"name": "Build Ups (up to 18inch) x2", "price": 335.99, "quantity": 1},
    {"name": "Build Ups Other (every 6\" after 18\")", "price": 34.99, "quantity": 1},
    {"name": "Build Up Other (up to 18\")", "price": 230.99, "quantity": 1},
    {"name": "C/1 Ring w/cover 24\" HD", "price": 435.99, "quantity": 1},
    {"name": "C/I Ring w/cover 18\"", "price": 314.99, "quantity": 1},
    {"name": "C/I Ring w/cover med 24\"", "price": 435.99, "quantity": 1},
    {"name": "CCLS", "price": 119.99, "quantity": 1},
    {"name": "Concrete Cover (21-27 inches)", "price": 125.99, "quantity": 1},
    {"name": "Concrete Cover (27-29 inches)", "price": 151.99, "quantity": 1},
    {"name": "Concrete Cover (36 inches)", "price": 199.99, "quantity": 1},
    {"name": "Concrete Cover (42 inches)", "price": 314.99, "quantity": 1},
    {"name": "Digging Fee", "price": 39.50, "quantity": 1},
    {"name": "Drain Master", "price": 125.99, "quantity": 1},
    {"name": "Emergency Fee (Weekday & Sat/Sun)", "price": 180.00, "quantity": 1},
    {"name": "Emergency Fee Holiday", "price": 295.00, "quantity": 1},
    {"name": "Extra Hose per hose 1st 3 free", "price": 27.00, "quantity": 1},
    {"name": "Handsnake", "price": 100.00, "quantity": 1},
    {"name": "High Velocity Water Snake 1/2 Rate", "price": 167.99, "quantity": 1},
    {"name": "High Velocity Water Snake 1st Rate", "price": 335.99, "quantity": 1},
    {"name": "High Velocity Water Snake Additional Hr", "price": 167.99, "quantity": 1},
    {"name": "Labor & Machine per Hour", "price": 180.00, "quantity": 1},
    {"name": "Poly 122 Filter Package with 1 Foot Riser", "price": 375.99, "quantity": 1},
    {"name": "Poly 122 Filter Package with 2 Foot Riser", "price": 440.99, "quantity": 1},
    {"name": "Poly-122 Filter", "price": 230.99, "quantity": 1},
    {"name": "Poly-Lok Green Plastic Cover (18\")", "price": 120.99, "quantity": 1},
    {"name": "Poly-Lok Green Plastic Cover (24\")", "price": 134.99, "quantity": 1},
    {"name": "Poly-Lok Green Plastic Cover (30\")", "price": 140.99, "quantity": 1},
    {"name": "Service Call", "price": 155.00, "quantity": 1},
    {"name": "System Eval Additional Hours", "price": 180.00, "quantity": 1},
    {"name": "System Eval 1st Hour", "price": 260.00, "quantity": 1},
    {"name": "Truck Time", "price": 195.00, "quantity": 1},
    {"name": "Truck Time OT", "price": 270.00, "quantity": 1},
    {"name": "Zable Filter", "price": 175.00, "quantity": 1},
    {"name": "Zabel Filter Package with 1 Foot Riser", "price": 304.99, "quantity": 1},
    {"name": "Zable Filter Package with 2 Foot riser", "price": 335.99, "quantity": 1},
]

def clear_invoices():
    Service.objects.all().delete()
    print("All services have been cleared from the database.")

def add_services():
    for service_data in services_data:
        Service.objects.create(**service_data)
    print("All services have been added to the database.")

if __name__ == "__main__":
    clear_invoices()
    add_services()
