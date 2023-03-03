# PayPal Payments Service
This folder contains the Django project for the PayPal Payments service.

It will include source code, DB schemas, documentation, tests and anything else that is needed to run the service.

The source code files can be found in `./paypal_service/`, and the automated test code files can be found in `./test/`.

# Creating the DBs
1. Run `python manage.py check` in this folder
2. Run `python manage.py makemigrations service` in this folder
3. Run `python manage.py migrate` in this folder