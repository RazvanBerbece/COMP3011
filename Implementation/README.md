# PayFriend Payments Service
This folder contains the Django project for the PayFriend Payments service.

It will include source code, DB schemas, documentation, tests and anything else that is needed to run the service.

The source code files can be found in `./payfriend_service/`.

# Creating the DBs
1. Run `python manage.py check` in folder `./payfriend_service/`
2. Run `python manage.py makemigrations service` in folder `./payfriend_service/`
3. Run `python manage.py migrate` in folder `./payfriend_service/`

# Running the tests
1. Run `python manage.py test` in folder `./payfriend_service/`

# Service Demo Account (To Process Payments) 
Email: `ammarcomp@leeds.com`
Password: `testpass12345678`