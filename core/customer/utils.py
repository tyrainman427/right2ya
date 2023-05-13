def calculate_job_price(job):
    if job.delivery_choice == job.SCHEDULED_DELIVERY:
        service_fee = 60.00
        delivery_fee = 0.25 * service_fee
        price = service_fee + delivery_fee
    else:
        print("Price saved!")
        price = job.price
        delivery_fee = 0.25 * price
        price = price + delivery_fee

    return price

def save(self, *args, **kwargs):
    if self.delivery_choice == self.SCHEDULED_DELIVERY:
        self.service_fee = 60.00
        self.delivery_fee = 0.25 * self.service_fee
        self.price = self.service_fee + self.delivery_fee
    else:
        print('save() is called.')
        self.delivery_fee = 0.25 * self.price
        self.price = self.price + self.delivery_fee
    
        self.price.save(*args, **kwargs)