import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from field_trans.models import Language
from django.db import transaction

# from feed.functions import validate_form_with_inlines

# from feed import functions
# from feed.functions import UPLOADS_DIR

from field_trans.helpers import set_translation, get_verbose_language

from . import models
from . import forms
from . import helpers
from microfeed2.forms import get_post_form


def list(request, page_category_id):
    context = {}
    oPageCategory = models.PageCategory.objects.get(pk=page_category_id)
    context['qCategory'] = models.PageCategory.objects.all().filter(parent=None)
    context['oPageCategory'] = oPageCategory
    context['hierarchy'] = oPageCategory.get_hierarchy()
    context['fPage'] = forms.PageForm(initial={'category':oPageCategory.id})
    return render(request, 'pages/list.html', context)


def view_page(request, page_id):
    context = {}
    PostForm = get_post_form()
    oPage = models.Page.visible_obj.get(pk=page_id)
    context['oPage'] = oPage
    context['fPost'] = PostForm(initial={'thread': oPage.post_thread})
    context['qCategory'] = models.PageCategory.objects.all().filter(parent=None)
    context['hierarchy'] = oPage.get_hierarchy()
    context['fPage'] = forms.PageForm(initial={'category':oPage.category.id})
    fEditpage = forms.PageForm()
    fEditpage.set_edit_page(oPage)
    context['fEditPage'] = fEditpage
    return render(request, 'pages/page.html', context)


@login_required
@transaction.atomic
def new_page(request):
    context = {}
    fPage = forms.PageForm()
    if request.method == 'POST':
        fPage = forms.PageForm(request.POST)
        if fPage.is_valid():
            oPage = fPage.save_page(request.user)
            messages.success( request, _('A new page was created.') )
            
            return redirect(reverse('pages:view_page', args=[oPage.id]))
    context['fPage'] = fPage
    return render(request, 'pages/new_page.html', context)

@login_required
@transaction.atomic
def edit_page(request, page_id):
    context = {}
    oPage = models.Page.objects.get(pk=page_id)
    fEditPage = forms.PageForm()
    fEditPage.set_edit_page(oPage)
    if request.method == 'POST':
        fEditPage = forms.PageForm(request.POST)
        fEditPage.set_edit_page(oPage)
        if fEditPage.is_valid():
            oPage = fEditPage.save_page(request.user, oPage)
            messages.success( request, _('This page has been edited successfully.') )
            return redirect(reverse('pages:view_page', args=[oPage.id]))
    context['fPage'] = fEditPage
    return render(request, 'pages/new_page.html', context)

@login_required
def translate_page(request, page_id):
    context = {}
    oPage = models.Page.visible_obj.all().get(pk=page_id)
    context['oPage'] = oPage
    if request.POST:
        language = request.POST.get('language')
        set_translation('page', 'title', oPage.id, language, request.POST.get('title'))
        set_translation('page', 'teaser', oPage.id, language, request.POST.get('teaser'))
        set_translation('page', 'body', oPage.id, language, request.POST.get('body'))
        messages.success( request, _('Page successfully translated.') )
        if oPage.category.show_as_page:
            return redirect('pages:list', page_category_id=oPage.category.id)
        return redirect('pages:view_page', page_id=oPage.id)
    qLanguage = Language.objects.all()
    context['qLanguage'] = qLanguage
    context['hierarchy'] = oPage.get_hierarchy()
    return render(request, 'pages/translate_page.html', context)

@login_required
def delete_page(request):
    page_id = int( request.POST.get('page_id') )
    oPage = models.Page.objects.all().get(id=page_id)
    parent_id = oPage.category.id
    oPage.delete()
    messages.success( request, _('Page successfully deleted.') )
    return redirect('pages:list', page_category_id=parent_id)

@login_required
def hide_page(request):
    page_id = int( request.POST.get('page_id') )
    oPage = models.Page.objects.all().get(id=page_id)
    parent_id = oPage.category.id
    oPage.visible = False
    oPage.save()
    messages.success( request, _('Page successfully removed.') )
    return redirect('pages:list', page_category_id=parent_id)

@login_required
def translate_category(request, category_id):
    context = {}
    oCategory = models.PageCategory.objects.all().get(pk=category_id)
    context['oCategory'] = oCategory
    if request.POST:
        language = request.POST.get('language')
        set_translation('page_category', 'title', oCategory.id, language, request.POST.get('title'))
        messages.success( request, _('Title successfully translated.') )
    qLanguage = Language.objects.all()
    context['qLanguage'] = qLanguage
    context['hierarchy'] = oCategory.get_hierarchy()
    return render(request, 'pages/translate_category.html', context)


@login_required
def new_category(request):
    context = {}
    initial = {}
    parent_id = request.GET.get('parent_id', None )
    if parent_id:
        initial = {'parent' : int( parent_id ) }
    form = forms.PageCategoryForm(initial=initial)
    if request.POST:
        form = forms.PageCategoryForm(request.POST)
        if form.is_valid():
            oPageCategory = form.save()
            messages.success(request, 'Successfully created category.')
            return redirect('pages:list', page_category_id=oPageCategory.id)
    context['form'] = form
    return render(request, 'pages/new_category.html', context)
    
@login_required
def edit_category(request, category_id):
    context = {}
    oPageCategory = models.PageCategory.objects.all().get(pk=category_id)
    form = forms.PageCategoryForm(instance=oPageCategory)
    if request.POST:
        form = forms.PageCategoryForm(request.POST, instance=oPageCategory)
        if form.is_valid():
            oPageCategory = form.save()
            messages.success(request, 'Successfully edited category.')
            return redirect('pages:list', page_category_id=category_id)
    context['form'] = form
    return render(request, 'pages/new_category.html', context)

### OLD ##########################################################

















def home(request):
    return HttpResponse("hello world")












    


