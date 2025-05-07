from typing import Any, Dict
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Property, PropertyBook, PropertyImages, Category, Place
from .forms import PropertyBookForm
from .filters import PropertyFilter
from django_filters.views import FilterView
# Create your views here.

class PropertyList(FilterView):
    model = Property
    paginate_by = 6
    filterset_class = PropertyFilter
    template_name = 'property/property_list.html' 


class PropertyDetail(FormMixin, DetailView):
    model = Property
    template_name = 'property/property_detail.html'
    form_class = PropertyBookForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related"] = Property.objects.filter(category=self.get_object().category)[:3]
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            myform = form.save(commit=False)
            myform.property = self.get_object()
            myform.user = request.user
            myform.save()
            
            return redirect('/')
        else:
            print('not valid')

@login_required
def add_listing(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'property/add_listing.html', context)

@login_required
def add_listing_submit(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        location = request.POST.get('location')
        description = request.POST.get('description')
        beds = request.POST.get('beds')
        baths = request.POST.get('baths')
        area = request.POST.get('area')
        max_guests = request.POST.get('max_guests')
        amenities = request.POST.getlist('amenities')
        
        # Validate required fields
        if not all([name, price, category_id, description]):
            messages.error(request, 'Please fill in all required fields')
            return redirect('property:add_listing')
        
        try:
            # Create new property
            category = Category.objects.get(id=category_id)
            
            property = Property.objects.create(
                name=name,
                price=price,
                category=category,
                places=Place.objects.first(),  # Default place, adjust as needed
                description=description,
                owner=request.user
            )
            
            # Handle main image
            if 'main_image' in request.FILES:
                main_image = request.FILES['main_image']
                property.image = main_image
                property.save()
            
            # Handle additional images
            if 'additional_images' in request.FILES:
                for image in request.FILES.getlist('additional_images'):
                    PropertyImages.objects.create(
                        property=property,
                        image=image
                    )
            
            messages.success(request, 'Your property has been listed successfully!')
            return redirect('property:property_detail', slug=property.slug)
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('property:add_listing')
    
    return redirect('property:add_listing')
