# COMP3011 - PayFriend Payment Service
Monorepo which holds the code and documentation for CW2 of the COMP3011 module.

# How to Run (Locally)
1. In `Implementation/payfriend_service/` run the `python manage.py runserver` command to start the service
2. Navigate to http://127.0.0.1:8000/admin/, which is the project admin site

# Local Database Access
Database acces is done through the admin site. 

**Note: The models needs to be specifically registered with the admin site by adding them into the `Implementation/payfriend_service/service/admin.py` file.**

# Local Testing
TODO

# CI/CD

# CI
The web service codebase is automatically tested on pull requests to the main branch, to ensure that there were no breaking changes made to the code and that the service still works as expected.

The automated testing workflow file can be found in `.github/workflows/test.yml`

# CD
The Django web service is going to be published on the public internet via deployment to PythonAnywhere.

The deployment process is automated and pushes the newest version of the service to PythonAnywhere on pushes to the main branch.

The automated deployment workflow file can be found in `.github/workflows/deploy.yml`