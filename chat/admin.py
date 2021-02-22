from django.contrib import admin
from .models import Conversations,ConversationMessage,Notifications

# Register your models here.
admin.site.register(Conversations)
admin.site.register(ConversationMessage)
admin.site.register(Notifications)
