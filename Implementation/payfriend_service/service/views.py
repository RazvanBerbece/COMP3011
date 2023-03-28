from datetime import *

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Message Types
from .classes.message.response.Response import Response
from .classes.message.response.PaymentResponse import PaymentResponse

# Microservices Interfaces
from .classes.component.auth.auth import AuthComponent
from .classes.component.pay.pay import PaymentComponent

# Create your views here.

def gateway(request):
    """
    Entrypoint for service. Used to check that service is up and running.
    """
    timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
    response = Response("/", None, {}, timestamp, 1)
    return JsonResponse(response.get_json(), safe = False)

@csrf_exempt 
def signup(request):
    """
    Endpoint to register a user on the service using an email and a password provided in a POST request form-body.
    """
    # Get POST body data
    email = request.POST.get('email')
    password = request.POST.get('password')
    # Inject service instance
    auth_service = AuthComponent()
    # Process
    status = auth_service.register_user(email, password)
    # Send response
    timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
    response = Response("/signup/", None, {}, timestamp, 1)
    if status == -1:
        # User already registered
        response._error = { "message": f"A user with the {email} email address already exists." }
        response.success = 0
        return JsonResponse(response.get_json(), safe = False)
    return JsonResponse(response.get_json(), safe = False)

@csrf_exempt 
def signin(request):
    """
    Endpoint to authenticate a user on the service using an email and a password provided in a POST request form-body.
    """
    # Get POST body data
    email = request.POST.get('email')
    password = request.POST.get('password')
    # Inject service instance
    auth_service = AuthComponent()
    # Process
    status = auth_service.authenticate_user(email, password)
    # Send response
    timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
    response = Response("/signin/", None, {}, timestamp, 1)
    if status == False:
        # User not registered
        response._error = { "message": f"A user with the {email} email does not exist." }
        return JsonResponse(response.get_json(), safe = False)
    return JsonResponse(response.get_json(), safe = False)

@csrf_exempt 
def pay(request):
    """
    Endpoint to request a payment processing using details provided in a POST request form-body.
    """
    # Get POST body data
    email = request.POST.get('email')
    password = request.POST.get('password')
    value = request.POST.get('value')
    company = request.POST.get('company')
    # Inject service instance
    payment_service = PaymentComponent()
    # Process payment details
    transaction, err = payment_service.process_payment(email, password, value, company)
    if err != None:
        # Payment failed to process
        timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
        response = Response("/pay/", None, { "message": err }, timestamp, 0)
        return JsonResponse(response.get_json(), safe = False)
    else:
        # Successful payment
        response = PaymentResponse(transaction["id"], None, transaction["timestamp"])
        return JsonResponse(response.get_json(), safe = False)