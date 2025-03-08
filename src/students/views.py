#student/views.py
from django.shortcuts import render
from django.contrib import messages
from .models import Contact
# def home(request):
#     return render(request, 'home.html', {'title': 'Crest Portal'})

def home(request):
    # Handle search form (GET request)
    search_query = request.GET.get('keyword', '')  # Get the 'keyword' parameter from the search form
    context = {
        'title': 'Crest Portal',
        'search_query': search_query,
    }
    if search_query:
        # Placeholder for search logic; for now, just pass the query back to the template
        context['search_message'] = f'Searching for: {search_query}'
        # Later, you can add logic to search a database or external API
    return render(request, 'home.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Save to database
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        # Placeholder for contact form handling (e.g., save to database, send email)
        messages.success(request, f'Thank you, {name}! Your message has been received.')
        return render(request, 'home.html', {'title': 'Crest Portal'})
    # If GET request, just render the home page (scrolling will take user to Contact Us section)
    return render(request, 'home.html', {'title': 'Crest Portal'})