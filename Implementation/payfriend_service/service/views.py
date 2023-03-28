from datetime import *

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Message Types
from .classes.message.response.Response import Response
from .classes.message.response.PaymentResponse import PaymentResponse

# Microservices Interfaces
from .classes.component.auth.auth import AuthService

# Create your views here.

def gateway(request):
    timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
    response = Response("/", None, {}, timestamp, 1)
    return JsonResponse(response.get_json(), safe = False)

@csrf_exempt 
def signup(request):
    # Get POST body data
    email = request.POST.get('email')
    password = request.POST.get('password')
    # Inject service instance
    auth_service = AuthService()
    # Process
    auth_service.register_user(email, password)
    # Send response
    timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
    response = Response("/signup/", None, {}, timestamp, 1)
    return JsonResponse(response.get_json(), safe = False)