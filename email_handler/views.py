from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from . import forms
from .helpers import send_system_mail
from main.helpers import constants



def composer(request):
    context = {}
    form = forms.ComposeEmailForm()
    if request.POST:
        form = forms.ComposeEmailForm(request.POST)
        if form.is_valid():
            print('send email')
            email_context = {
                'name' : form.cleaned_data['user'].get_short_name(),
                'body' : form.cleaned_data['body'],
                'subject' : form.cleaned_data['subject'],
                'unsubscribe_code' : 12345             
            }
            recipient_email = form.cleaned_data['user'].email
            message = render_to_string('email_handler/email_generic.txt', email_context, request)
            html_message = render_to_string('email_handler/email_generic.html', email_context, request)
            if 'send_email' in request.POST:
                send_system_mail(
                    subject = form.cleaned_data['subject'],
                    message = message,
                    html_message = html_message,
                    from_mail = constants['CONTACT_EMAIL'],
                    to_list = [recipient_email]                     
                )
                messages.success(request, 'Email sent.')
            context['message'] = message
            context['html_message'] = html_message
            context['recipient_email'] = recipient_email
            context['subject'] = form.cleaned_data['subject']
    context['form'] = form
    return render(request, 'email_handler/composer.html', context)

def unsubscribe(request, code):
    context = {}
    return render(request, 'email_handler/unsubscribe.html', context)