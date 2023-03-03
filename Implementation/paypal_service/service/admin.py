from django.contrib import admin
from .models import Transaction, Card

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Card)