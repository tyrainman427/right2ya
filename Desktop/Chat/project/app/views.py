from django.shortcuts import render

def index(request):
    return render(request, "index.html", {})

def chat_box(request, room_name):
    # we will get the chatbox name from the url
    return render(request, "chatbox.html", {"room_name": room_name})