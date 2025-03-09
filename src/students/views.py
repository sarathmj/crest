#students/views.py
import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
import logging
from .models import Contact, ActivityLog
from django.db import IntegrityError

logger = logging.getLogger('students')

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
        # Added: Log search activity
        ip_address = request.META.get('REMOTE_ADDR')
        session_key = request.session.session_key
        logger.info(f"Search performed: {search_query} from IP {ip_address}")
        ActivityLog.objects.create(
            action="Search Performed",
            details=f"Search query: {search_query}",
            ip_address=ip_address,
            session_key=session_key
        )
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
                # Added: Log successful form submission
                ip_address = request.META.get('REMOTE_ADDR')
                session_key = request.session.session_key
                logger.info(f"Contact form submitted by {name} ({email}) from IP {ip_address}")
                ActivityLog.objects.create(
                    action="Contact Form Submission",
                    details=f"Submitted by {name} ({email}): {message}",
                    ip_address=ip_address,
                    session_key=session_key
                )
                messages.success(request, f'Thank you, {name}! Your message has been received.')
                # Clear the token after successful submission
                del request.session['contact_form_token']
                request.session['contact_form_token'] = str(uuid.uuid4())
            except IntegrityError as e:
                # Added: Log IntegrityError
                ip_address = request.META.get('REMOTE_ADDR')
                session_key = request.session.session_key
                logger.warning(f"Duplicate submission detected: {str(e)} from IP {ip_address}")
                ActivityLog.objects.create(
                    action="Duplicate Submission",
                    details=f"Duplicate submission by {name} ({email}): {str(e)}",
                    ip_address=ip_address,
                    session_key=session_key
                )
                messages.warning(request, 'This message has already been submitted.')
            return redirect('home')
        else:
            # Added: Log invalid form submission
            ip_address = request.META.get('REMOTE_ADDR')
            session_key = request.session.session_key
            logger.warning(f"Invalid form submission: Token mismatch from IP {ip_address}")
            ActivityLog.objects.create(
                action="Invalid Form Submission",
                details="Token mismatch",
                ip_address=ip_address,
                session_key=session_key
            )
            messages.error(request, 'Invalid form submission.')
            return redirect('home')
    return render(request, 'home.html', {'title': 'Crest Portal'})