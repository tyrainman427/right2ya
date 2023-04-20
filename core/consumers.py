import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from . import models

class JobConsumer(WebsocketConsumer):
  def connect(self):
    self.job_id = self.scope['url_route']['kwargs']['job_id']
    self.job_group_name = 'job_%s' % self.job_id
    self.job = models.Job.objects.get(id=self.job_id)

    # Join room group
    async_to_sync(self.channel_layer.group_add)(
      self.job_group_name,
      self.channel_name
    )
    print("Joining room")
    self.accept()
    
  def receive(self, text_data):
    print("sending message to the group")
    data = json.loads(text_data)
    job = data.get('job')

    if job:
        courier = self.scope['user'].courier
        if 'courier_lat' in job:
            courier.lat = job['courier_lat']
        if 'courier_lng' in job:
            courier.lng = job['courier_lng']
        courier.save()
        job['courier'] = {'lat': courier.lat, 'lng': courier.lng}

        # Send message to job group
        async_to_sync(self.channel_layer.group_send)(
            self.job_group_name,
            {
                'type': 'job_update',
                'job': job,
            }
        )
    else:
        print('Invalid job data')

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
  def job_update(self, event):

    # Send message to WebSocket
    self.send(text_data=json.dumps(event))
    
  def disconnect(self, close_code):
        # Leave room group
    async_to_sync(self.channel_layer.group_discard)(
      self.job_group_name,
      self.channel_name
    )
    print("Leaving room")
