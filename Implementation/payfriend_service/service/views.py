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
    return JsonResponse(response.get_json(), safe = False, status = 200)

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
            return JsonResponse(response.get_json(), safe = False, status = 501)
        elif status == -2:
            # Invalid email address
            response._error = { "message": f"The provided email address {email} is invalid to use for registration." }
            response.success = 0
            return JsonResponse(response.get_json(), safe = False, status = 402)
        elif status == -3:
            # Invalid password
            response._error = { "message": f"The provided password is too weak to use for registration." }
            response.success = 0
            return JsonResponse(response.get_json(), safe = False, status = 402)
    return JsonResponse(response.get_json(), safe = False, status = 201)

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
            return JsonResponse(response.get_json(), safe = False, status = 502)
        elif status == -2:
            # Invalid email address
            response._error = { "message": f"The provided email address {email} is invalid to use for signin." }
            response.success = 0
            return JsonResponse(response.get_json(), safe = False, status = 402)
        elif status == -3:
            # Invalid email address
            response._error = { "message": f"The provided password is not valid to use for signin." }
            response.success = 0
            return JsonResponse(response.get_json(), safe = False, status = 402)
    return JsonResponse(response.get_json(), safe = False, status = 200)

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
    city = request.POST.get('city')
    postcode = request.POST.get('postcode')
    country = request.POST.get('country')
    currency = request.POST.get('currency')
    # Inject component instances
    payment_component = PaymentComponent()
    # Process payment details and login credentials
    transaction, err = payment_component.process_payment(email, password, value, company, city, postcode, country, currency)
    if err != None:
        # Payment failed to process
        timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
        response = Response("/pay/", None, { "message": err }, timestamp, 0)
        return JsonResponse(response.get_json(), safe = False, status = 500)
    else:
        # Successful payment
        response = PaymentResponse(transaction["id"], None, transaction["timestamp"])
        return JsonResponse(response.get_json(), safe = False, status = 200)

@csrf_exempt 
def transactions(request, transactionId: str):
    """
    Endpoint to request a transaction operation (READ, DELETE) in the store using details provided in the URL path.
    """
    if request.method == 'DELETE':
        # Inject component instances
        payment_component = PaymentComponent()
        # Remove transaction
        status = payment_component.delete_payment(transactionId)
        if (status < 0):
            if (status == -1):
                # Transaction not found
                timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
                response = Response(f"/{transactionId}", transactionId, { "message": f"Transaction with ID {transactionId} not found in store." }, timestamp, 0)
                return JsonResponse(response.get_json(), safe = False, status = 503)
            elif (status == -2):
                # Transaction id not valid
                timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
                response = Response(f"/{transactionId}", transactionId, { "message": f"Transaction ID {transactionId} is invalid." }, timestamp, 0)
                return JsonResponse(response.get_json(), safe = False, status = 406)
        # Transaction deletion successful
        timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
        response = Response(f"/{transactionId}", transactionId, {}, timestamp, 1)
        return JsonResponse(response.get_json(), safe = False, status = 202)
    else:
        timestamp = datetime.now(timezone.utc).timestamp() * 1000 # in milliseconds since Unix epoch
        response = Response(f"/{transactionId}", transactionId, { "message": f"Method {request.method} not allowed for resource path /{transactionId}." }, timestamp, 0)
        return JsonResponse(response.get_json(), safe = False, status = 420)