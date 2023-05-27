import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . import models
from channels.db import database_sync_to_async
from django.http import JsonResponse

class JobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.job_group_name = f'job_{self.job_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.job_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.job_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        job = text_data_json.get('job')

        if job and 'courier_lat' in job and 'courier_lng' in job:
            lat = job['courier_lat']
            lng = job['courier_lng']

            if self.validate_coordinates(lat, lng):
                await self.save_courier_location(lat, lng)
                # Send message to job group
                await self.channel_layer.group_send(
                    self.job_group_name,
                    {
                        'type': 'job_update',
                        'job': job,
                    }
                )
            else:
                error_message = {
                    'error': 'Invalid courier coordinates',
                }
                await self.send(text_data=json.dumps(error_message))
        else:
            error_message = {
                'error': 'Invalid job data',
            }
            await self.send(text_data=json.dumps(error_message))

    async def job_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_courier_location(self, lat, lng):
        courier = self.scope['user'].courier
        courier.lat = lat
        courier.lng = lng
        courier.save()

    def validate_coordinates(self, lat, lng):
        try:
            lat = float(lat)
            lng = float(lng)
            if -90 <= lat <= 90 and -180 <= lng <= 180:
                return True
            else:
                return False
        except ValueError:
            return False
