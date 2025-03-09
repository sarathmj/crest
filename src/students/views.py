import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.db import IntegrityError

def home(request):
    if 'contact_form_token' not in request.session:
        request.session['contact_form_token'] = str(uuid.uuid4())
    search_query = request.GET.get('keyword', '')
    context = {
        'title': 'Crest Portal',
        'search_query': search_query,
        'contact_form_token': request.session['contact_form_token'],
    }
    if search_query:
        context['search_message'] = f'Searching for: {search_query}'
    return render(request, 'home.html', context)

def contact(request):
    if request.method == 'POST':
        token = request.POST.get('contact_form_token')
        if token and token == request.session.get('contact_form_token'):
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            try:
                contact = Contact(name=name, email=email, message=message)
                contact.save()
                messages.success(request, f'Thank you, {name}! Your message has been received.')
                # Clear the token after successful submission
                del request.session['contact_form_token']
                request.session['contact_form_token'] = str(uuid.uuid4())
            except IntegrityError as e:
                messages.warning(request, 'This message has already been submitted.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid form submission.')
            return redirect('home')
    return render(request, 'home.html', {'title': 'Crest Portal'})