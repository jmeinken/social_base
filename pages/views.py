import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

# from feed.functions import validate_form_with_inlines

# from feed import functions
# from feed.functions import UPLOADS_DIR

from field_trans.helpers import set_translation, get_verbose_language

from . import models
from . import forms


def list(request, page_category_id):
    context = {}
    oPageCategory = models.PageCategory.objects.get(pk=page_category_id)
    context['oPageCategory'] = oPageCategory
    return render(request, 'pages/list.html', context)


def view_page(request, page_id):
    context = {}
    oPage = models.Page.visible_obj.get(pk=page_id)
    context['oPage'] = oPage
    return render(request, 'pages/page.html', context)


### OLD ##########################################################














page_titles = {
    'restaurant' : _('Restaurants'),
    'local_destination' : _('Local Destinations'),
    'regional_destination' : _('Regional Destinations'),
    'housing' : _('Housing'),
    'shopping' : _('Shopping'),
    'medical' : _('Medical'),
    'transportation' : _('Transportation'),
    'education' : _('Education'),
}


def home(request):
    return HttpResponse("hello world")




@login_required
def new_page(request):
    context = {}
    form = forms.PageForm()
    children = [forms.PageLinkFormSet]
    if request.method == 'POST':
        form, children, is_valid = validate_form_with_inlines(form, children, request.POST)
        if is_valid:
            oPage = form.save(commit=False)
            oPage.user = request.user
            oPage.save()
            for child in children:
                child.instance = oPage
                child.save()
            messages.success( request, _('Page successfully added.') )
            return redirect('pages:page', page_id=oPage.id)
    context['form'] = form
    context['children'] = children
    return render(request, 'pages/new_page.html', context)

@csrf_exempt
def delete_page(request):
    page_id = int( request.POST.get('page_id') )
    oPage = models.Page.objects.all().get(id=page_id)
    oPage.visible = False
    oPage.save()
    messages.success( request, _('Page successfully deleted.') )
    return redirect('home')


@login_required
def edit_page(request, page_id):
    context = {}
    oPage = get_object_or_404(models.Page, pk=page_id)
    if not oPage.visible:
        raise Http404("Page has been deleted.")
    form = forms.PageForm(instance=oPage)
    children = [forms.PageLinkFormSet]
    if request.method == 'POST':
        form, children, is_valid = validate_form_with_inlines(form, children, request.POST, oPage)
        if is_valid:
            oPage = form.save(commit=False)
            oPage.user = request.user
            oPage.save()
            for child in children:
                child.instance = oPage
                child.save()
            messages.success( request, _('Page successfully edited.') )
            return redirect('pages:page', page_id=oPage.id)
    else:
        temp_children = []
        for child in children:
            temp_children.append( child(instance=oPage) )
        children = temp_children
    context['form'] = form
    context['children'] = children
    return render(request, 'pages/new_page.html', context)

@login_required
def translate_page(request, page_id):
    context = {}
    oPage = models.Page.visible_obj.all().get(pk=page_id)
    if request.method == 'POST':
        language = request.POST.get('language')
        title = request.POST.get('title', '')
        body = request.POST.get('body', '')
        teaser = request.POST.get('teaser', '')
        set_translation('page', 'title', oPage.id, language, title)
        set_translation('page', 'body', oPage.id, language, body)
        set_translation('page', 'teaser', oPage.id, language, teaser)
        messages.success( request, _('Page successfully translated.') )
        return redirect('pages:page', page_id=oPage.id)
    context['oPage'] = oPage
    lang = request.GET.get('language')
    if lang:
        context['language'] = lang
    else:
        context['language'] = request.LANGUAGE_CODE
    context['verbose_language'] = get_verbose_language(context['language'])
    return render(request, 'pages/translate_page.html', context)
    

def page(request, page_id):
    context = {}
    context['upcoming_events'] = functions.get_upcoming_events()
    oPage = models.Page.visible_obj.all().get(pk=page_id)
    context['oPage'] = oPage
    context['verbose_language'] = get_verbose_language(request.LANGUAGE_CODE)
    return render(request, 'pages/page.html', context)



@csrf_exempt
def upload_image(request):
    context = {}
    if request.method == 'POST':
        image = request.POST.get('image')
        if image:
            imageArr = image.split(',')
            i = 0
            while os.path.exists(UPLOADS_DIR + 'page_images/image_' + str(i) + '.png'):
                i += 1
            image_name = 'image_' + str(i) + '.png'     # placeholder
            image_path = '/static/uploads/page_images/' + image_name
            fh = open(UPLOADS_DIR + "page_images/" + image_name, "wb")
            fh.write(imageArr[1].decode('base64'))
            fh.close()
            return HttpResponse(json.dumps(image_path), content_type = "application/json")
    return HttpResponse(json.dumps('fail'), content_type = "application/json")
    


