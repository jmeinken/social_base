from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string  #render_to_string(template_name, context=None, request=None, using=None)






@login_required
def translate(request):
    context = {}
    response = {}
    
    response['html'] = render_to_string('field_trans/blocks/translate.html', context, request)
    
    return JsonResponse(response, safe=False)