from django.urls import path
from .views import *

app_name = 'clients'

urlpatterns = [
    path('', ClientList.as_view(), name='clients_list'),
    path('<int:id>/', ClientDetailView.as_view(), name='file_detail'),
    path('new/', ClientCreateView.as_view(), name='client-create'),
    path('<pk>/update-client/', ClientUpdateView.as_view(), name='client-update'),
    path('<pk>/delete-client/', ClientDeleteView.as_view(), name='client-delete'),
    path('upload/', UploadFileView.as_view(), name='upload'),
    path('note/', NotesCreateView.as_view(), name='note-create'),
    path('note/<int:id>', NoteDetailView.as_view(), name='note_detail'),
]
