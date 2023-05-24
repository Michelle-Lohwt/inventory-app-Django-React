from django.contrib import admin
from .models import Inventory, InventoryGroup, Shop

# Register your models here.
admin.site.register((Inventory, InventoryGroup, Shop))
# This allows you to manage and interact with the data of these models through the admin interface.
# By registering the models, you can perform CRUD (Create, Read, Update, Delete) operations on the model instances, 
# view and edit their fields, and perform other administrative tasks.