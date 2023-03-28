from datetime import *

# Django imports
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Message Types
from .classes.message.response.Response import Response
from .classes.message.response.PaymentResponse import PaymentResponse

# Component Interfaces
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
    # Inject component instances
    auth_component = AuthComponent()
    # Process
    status = auth_component.register_user(email, password)
    # Send response
    timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
    response = Response("/signup/", None, {}, timestamp, 1)
    if status < 0:
        if status == -1:
            # User already registered
            response._error = { "message": f"A user with the {email} email address already exists." }
            response.success = 0
            return JsonResponse(response.get_json(), safe = False)
        elif status == -2:
            # Invalid email address
            response._error = { "message": f"The provided email address {email} is invalid to use for registration." }
            response.success = 0
            return JsonResponse(response.get_json(), safe = False)
        elif status == -3:
            # Invalid email address
            response._error = { "message": f"The provided password is too weak to use for registration." }
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
    # Inject component instances
    auth_component = AuthComponent()
    # Authenticate
    status = auth_component.authenticate_user(email, password)
    # Send response
    timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
    response = Response("/signin/", None, {}, timestamp, 1)
    if status < 0:
        if status == -1:
            # User not registered
            response._error = { "message": f"A user with the provided credentials does not exist." }
            response.success = 0
            return JsonResponse(response.get_json(), safe = False)
        elif status == -2:
            # Invalid email address
            response._error = { "message": f"The provided email address {email} is invalid to use for signin." }
            response.success = 0
            return JsonResponse(response.get_json(), safe = False)
        elif status == -3:
            # Invalid email address
            response._error = { "message": f"The provided password is not valid to use for signin." }
            response.success = 0
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
    # Inject component instances
    payment_component = PaymentComponent()
    # Process payment details and login credentials
    transaction, err = payment_component.process_payment(email, password, value, company)
    if err != None:
        # Payment failed to process
        timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
        response = Response("/pay/", None, { "message": err }, timestamp, 0)
        return JsonResponse(response.get_json(), safe = False)
    else:
        # Successful payment
        response = PaymentResponse(transaction["id"], None, transaction["timestamp"])
        return JsonResponse(response.get_json(), safe = False)

@csrf_exempt 
def delete(request, transactionId: str):
    """
    Endpoint to request a transaction deletion from the store using details provided in the URL path.
    """
    # Inject component instances
    payment_component = PaymentComponent()
    # Remove transaction
    status = payment_component.delete_payment(transactionId)
    if (status == False):
        # Transaction not found or deletion failed
        timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
        response = Response(f"/{transactionId}", transactionId, { "message": f"Transaction with ID {transactionId} failed to be removed from store." }, timestamp, 0)
        return JsonResponse(response.get_json(), safe = False)
    # Transaction deletion successful
    timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
    response = Response(f"/{transactionId}", transactionId, {}, timestamp, 1)
    return JsonResponse(response.get_json(), safe = False)