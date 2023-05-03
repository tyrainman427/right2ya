import json
import asyncio
from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from . import models
from channels.db import database_sync_to_async
import threading

class JobConsumer(AsyncConsumer):
  async def websocket_connect(self, event):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.job_group_name = 'job_%s' % self.job_id
        # self.job = models.Job.objects.get(id=self.job_id)
        job_id = self.job_id
        
        # Join room group
        await self.channel_layer.group_add(
        self.job_group_name,
        self.channel_name
      )
        
        await self.send({
            "type": "websocket.accept",
        })
        

  async def websocket_receive(self, event):
    text_data = event.get('text', None)

    print("receive", text_data)
    if text_data is not None:
        text_data_json = json.loads(text_data)
        joblat = text_data_json.get('courier_lat')
        joblon = text_data_json.get('courier_lng')
        print(f"received job: ", joblat, joblon)

        if joblat and joblon:
            self.save_courier_location(joblat, joblon)
            print("location saved")
            
        myResponse = {
          'courier_lat': joblat,
          'courier_lng': joblon
        }
        
        test = json.dumps(myResponse)
        
        if event['type'] == 'websocket.send':
            await handle_websocket_send(test)
        
        # new_event = {
        #     "type": "websocket.send",
        #     "text": 
        
        # }

        # await self.channel_layer.group_send(
        #   self.job_group_name,     
        #      new_event
        # )
    async def handle_websocket_send(self,message):
    # Process the message here
      print("Received message:", message)

    # In this example, we simply send the message to the WebSocket group
      await self.channel_layer.group_send(
        self.job_group_name, {
            'type': 'send_message',
            'text':message
        }
    )

        
  def save_courier_location(self, lat, lng):
    def save_location():
        courier = self.scope['user'].courier
        print("Courier", courier)
        courier.lat = lat
        courier.lng = lng
        courier.save()
       

    thread = threading.Thread(target=save_location)
    thread.start()
    
  async def job_update(self, event, type='job_update'):
    # Send message to WebSocket
    await self.send(json.dumps(event))
    print("Sent message")
    
  # def save_courier_location(self, lat, lng):
  #   print("This is saving the location data")
  #   courier = self.scope['user'].courier
  #   print("Courier", courier)
  #   courier.lat = lat
  #   courier.lng = lng
  #   courier.save()
    


    



   
    
  # async def receive(self, text_data,event):
  #   print("received", event)
  
  # async def job_update(self, event):

  #   # Send message to WebSocket
  #   self.send(text_data=json.dumps(event))
  
    
  async def websocket_disconnect(self,event):
    print("disconnected", event)
    await self.channel_layer.group_discard(
        self.job_group_name,
        self.channel_name
    )
    
    
    # data = json.loads(text_data)
    # job = data.get('job')
    # print("sending message to the group",event)

    # if job:
    #     courier = self.scope['user'].courier
    #     if 'courier_lat' in job:
    #         courier.lat = job['courier_lat']
    #     if 'courier_lng' in job:
    #         courier.lng = job['courier_lng']
    #     courier.save()
    #     job['courier'] = {'lat': courier.lat, 'lng': courier.lng}

    #     # Send message to job group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.job_group_name,
    #         {
    #             'type': 'job_update',
    #             'job': job,
    #         }
    #     )
    # else:
    #     print('Invalid job data')

  # def receive(self, text_data):
  #   text_data_json = json.loads(text_data)
  #   job = text_data_json['job']
  #   print("received job")
  #   print("Job", job)

  #   if job.get('courier_lat') and job.get('courier_lng'):
  #     self.scope['user'].courier.lat = job['courier_lat']
  #     self.scope['user'].courier.lng = job['courier_lng']
  #     self.scope['user'].courier.save()

  #   # Send message to job group
  #   async_to_sync(self.channel_layer.group_send)(
  #     self.job_group_name,
  #     {
  #       'type': 'job_update',
  #       'job': job
  #     }
  #   )
    
    

  # Receive message from job group
    
  
@database_sync_to_async 
def get_thread(self,user,job_id):
  return models.Thread.objects.get_or_new(user,job_id)[0]