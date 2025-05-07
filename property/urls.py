from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    path('', views.PropertyList.as_view(), name='property_list'),
    path('<slug:slug>', views.PropertyDetail.as_view(), name='property_detail'),
    path('add-listing/', views.add_listing, name='add_listing'),
    path('add-listing/submit/', views.add_listing_submit, name='add_listing_submit'),
]
