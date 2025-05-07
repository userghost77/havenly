from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.home_search, name='home_search'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('contact-submit/', views.contact_submit, name='contact_submit'),
    path('category/<slug:category>', views.category_filter, name='category_filter'),
    path('chatbot/', views.chatbot, name='chatbot'),
]
