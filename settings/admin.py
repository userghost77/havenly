from django.contrib import admin
from .models import Chat, Settings  # Import directly from .models

# Register your models here
admin.site.register(Chat)
admin.site.register(Settings)
