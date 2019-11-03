from django.contrib import admin
from .models import messageModel, roomModel, userModel

# Register your models here.
admin.site.register(messageModel)
admin.site.register(userModel)
admin.site.register(roomModel)