import json
from django.shortcuts import render,redirect
from django.views import View
from django.db.models import Q
from .models import *
from django.core.mail import send_mail
# Create your views here.

class Index(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'customer/index.html')
    
class About(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'customer/about.html')
    
class Order(View):
    def get(self,request,*args, **kwargs):
        # get every items from each category
        visuals = MenuItem.objects.filter(category__name__contains='Visuals')
        time = MenuItem.objects.filter(category__name__contains='Time')
        photo = MenuItem.objects.filter(category__name__contains='Photo')
        lights = MenuItem.objects.filter(category__name__contains='Lights')
        type_of_payments = OrderModel.objects.all()
        
        # pass into context
        context = {
            'visuals':visuals,
            'time': time,
            'photo': photo,
            'lights': lights,
            'type_of_payments':type_of_payments,  
        }
        
        #render the template
        return render(request, 'customer/order.html', context)
    
    def post(self,request,*args, **kwargs):
        client_full_name = request.POST.get('client_full_name')
        contact_person = request.POST.get('contact_person')
        address = request.POST.get('address')
        telephone_number = request.POST.get('telephone_number')
        cell_number = request.POST.get('cell_number')
        date_of_event = request.POST.get('date_of_event')
        event_type = request.POST.get('event_type')
        number_of_guests= request.POST.get('number_of_guests')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location_of_event= request.POST.get('location_of_event')
        phone_number= request.POST.get('phone_number')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        
        order_items = {
            'items': []
        }
        items = request.POST.getlist('items[]')
        
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
            order_items['items'].append(item_data)
            
            price = 0
            item_ids = []
            
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
            
        order = OrderModel.objects.create(
            price=price,
            client_full_name=client_full_name,
            contact_person=contact_person,
            address=address,
            email=email,
            telephone_number=telephone_number,
            date_of_event=date_of_event,
            event_type=event_type, 
            number_of_guests=number_of_guests, 
            start_time=start_time,
            end_time=end_time, 
            location_of_event=location_of_event, 
            phone_number=phone_number,
            cell_number=cell_number,
            city=city,
            state=state,
            zip_code=zip_code
            )
        order.items.add(*item_ids)
        
        # send confirmation email to user
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order')
        
        send_mail(
            'Thank you for your order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )
        
        context = {
            'items': order_items['items'],
            'price': price
        }
        
        return redirect('order-confirmation', pk=order.pk)
    
class OrderConfirmation(View):
    def get(self,request,pk,*args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        
        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price
        }
        
        return render(request, 'customer/order_confirmation.html', context)
    
    def post(self,request,pk,*args, **kwargs):
        data = json.loads(request.body)
        if data['is_paid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()
            
        return redirect('payment-confirmation')
            
            
class OrderPayConfirmation(View):
    def get(self,request,*args, **kwargs):
        return render(request,'customer/order_pay_confirmation.html')
    

class Menu(View):
    def get(self,request,*args, **kwargs):
        menu_items = MenuItem.objects.all()
        
        context = {
            'menu_items': menu_items,
        }
        
        return render(request, 'customer/menu.html', context)
    
class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)