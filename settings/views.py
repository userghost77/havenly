import os
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Chat, Settings
from groq import Groq  # Import the correct class

# Set up logging
logger = logging.getLogger(__name__)

# Hardcode the API key directly (for testing only)
# In production, use environment variables
API_KEY = "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"  # Replace with your actual API key

# Initialize the client with the correct class
client = Groq(api_key=API_KEY)

def home(request):
    # Add your home view logic here
    context = {
        'places': [],  # Add your places data here
        'categories': [],  # Add your categories data here
        'places_list': [],  # Add your places_list data here
        'hotels_list': [],  # Add your hotels_list data here
        'resturant_list': [],  # Add your restaurant_list data here
    }
    return render(request, 'settings/home.html', context)

def home_search(request):
    # Add your home search logic here
    context = {
        'property_list': [],  # Add your property_list data here
    }
    return render(request, 'settings/home_search.html', context)

def category_filter(request, category):
    # Add your category filter logic here
    context = {
        'category': category,
        'property_list': [],  # Add your property_list data here
    }
    return render(request, 'settings/category_filter.html', context)

def contact_us(request):
    # Just render the contact form
    return render(request, 'settings/contact.html')

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # Form validation
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all fields')
            return redirect('settings:contact_us')
        
        # Instead of sending email, just log the message
        print(f"Contact form submission: {name} ({email}): {subject}")
        print(f"Message: {message}")
        
        # Success message
        messages.success(request, 'Your message has been sent. Thank you!')
        return redirect('settings:contact_us')
    
    # If not POST, redirect to contact page
    return redirect('settings:contact_us')

def ask_groqcloud(message):
    try:
        # Print for debugging
        print(f"Using API key: {API_KEY[:5]}...{API_KEY[-5:] if len(API_KEY) > 10 else ''}")
        
        # Try with a different model name
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Changed model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Groq API error: {str(e)}")
        print(f"DETAILED ERROR: {str(e)}")  # Print detailed error for debugging
        return f"Sorry, I encountered an error: {str(e)}"

@login_required
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()

        if message:
            try:
                # Get response from Groq
                response = ask_groqcloud(message)
                
                # Save to database
                chat = Chat(user=request.user, message=message, response=response)
                chat.save()
                
                # Return JSON response
                return JsonResponse({'message': message, 'response': response})
            except Exception as e:
                logger.error(f"Groq API call failed: {str(e)}")
                return JsonResponse({'error': f'Failed to get response from AI: {str(e)}', 'response': 'Sorry, I encountered an error. Please try again later.'}, status=500)
        else:
            return JsonResponse({'error': 'Empty message', 'response': 'Please type a message.'}, status=400)
    
    # For GET requests, render the chatbot template with chat history
    chats = Chat.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    # Print for debugging
    print(f"Rendering chatbot.html with {len(chats)} chats")
    
    return render(request, 'chatbot.html', {'chats': chats})

