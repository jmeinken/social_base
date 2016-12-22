from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

from . import forms
from microfeed import models




@login_required
def home(request):
    context = {}
    context['fPost'] = forms.PostForm()
    return render(request, 'microfeed2/home.html', context)

@login_required
def ajax_posts(request):
    '''Returns the html for a collection of posts.
    '''
    qPost = models.Post.objects.all()[:10]
    context = {  
       'qPost' : qPost,        
    }
    html = render_to_string('microfeed2/blocks/feed.html', context, request)
    response = {}
    response['html'] = html
    return JsonResponse(response, safe=False)
    