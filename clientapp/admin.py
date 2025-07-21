from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'contact_name', 'client_code', 'contact_number']

admin.site.register(Client, ClientAdmin)
