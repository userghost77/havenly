from django.urls import path
from settings import views  # Import from the correct app

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
]