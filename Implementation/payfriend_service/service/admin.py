from django.contrib import admin
from .models import Transaction, User

# Register your models here.
admin.site.register(Transaction)
admin.site.register(User)