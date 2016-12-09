import json


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404
from django.contrib import messages

from . import models
from . import functions
from . import forms
from main.helpers import constants

@csrf_exempt
def home(request):
    data = "hello world from microfeed"
    return HttpResponse(json.dumps(data), content_type = "application/json")


@csrf_exempt
def ajax_posts(request):
    currentUid = request.user.id
    last_post_id = int( request.GET.get('last_post_id') )
    post_count = int( request.GET.get('post_count') )
    thread = int( request.GET.get('thread', 1) )
    oThread = models.PostThread.objects.get(pk=thread)
    if last_post_id == 0:
        qPost = oThread.post_set.all().filter().order_by('-created')[:post_count]
    else:
        qPost = oThread.post_set.all().filter(id__lt=last_post_id).order_by('-created')[:post_count]
    response = []
    for oPost in qPost:
        x = oPost.objectify(currentUid)
        response.append(x)
    return HttpResponse(json.dumps(response), content_type = "application/json")

#def javascript_templates(request):
#    context = {}
#    return render(request, 'microfeed/javascript_templates.html', context)

def view_post(request, post_id):
    context = {}
    oPost = get_object_or_404(models.Post, pk=post_id)
    context['oPost'] = oPost
    return render(request, 'microfeed/view_post.html', context)

def new_event(request):
    context = {}
    fPost = forms.PostForm()
    fEventPost = forms.EventPostForm()
    sEventPostTime = forms.EventPostTimeFormSet()
    if request.method == 'POST':
        fPost = forms.PostForm(request.POST)
        fEventPost = forms.EventPostForm(request.POST)
        sEventPostTime = forms.EventPostTimeFormSet(request.POST)
        if fPost.is_valid() and fEventPost.is_valid() and sEventPostTime.is_valid():
            oPost = fPost.save(commit=False)
            oPost.user = request.user
            oPost.save()
            oEventPost = fEventPost.save(commit=False)
            oEventPost.post = oPost
            oEventPost.save()
            sEventPostTime.instance = oEventPost
            qEventPostTime = sEventPostTime.save()
            messages.success(request, 'Event successfully added.')
            return redirect('home')
    context = {
        'fPost' : fPost,
        'fEventPost' : fEventPost  ,
        'sEventPostTime' :  sEventPostTime        
    }
    return render(request, 'microfeed/new_event.html', context)

def edit_event(request, post_id):
    context = {}
    oPost = get_object_or_404(models.Post, pk=post_id)
    fPost = forms.PostForm(instance=oPost)
    oEventPost = get_object_or_404(models.EventPost, pk=post_id)
    fEventPost = forms.EventPostForm(instance=oEventPost)
    sEventPostTime = forms.EventPostTimeFormSet(instance=oEventPost)
    if request.method == 'POST':
        fPost = forms.PostForm(request.POST, instance=oPost)
        fEventPost = forms.EventPostForm(request.POST, instance=oEventPost)
        sEventPostTime = forms.EventPostTimeFormSet(request.POST, instance=oEventPost)
        if fPost.is_valid() and fEventPost.is_valid() and sEventPostTime.is_valid():
            oPost = fPost.save(commit=False)
            oPost.user = request.user
            oPost.save()
            oEventPost = fEventPost.save(commit=False)
            oEventPost.post = oPost
            oEventPost.save()
            sEventPostTime.instance = oEventPost
            qEventPostTime = sEventPostTime.save()
            messages.success(request, 'Event successfully edited.')
            return redirect('home')
    context = {
        'fPost' : fPost,
        'fEventPost' : fEventPost,
        'sEventPostTime' :  sEventPostTime                 
    }
    return render(request, 'microfeed/new_event.html', context)



@csrf_exempt
def get_post(request, post_id):
    data = "get post" + str(post_id)
    return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def new_post(request):
    currentUid = int( request.POST.get('uid') )
    images = request.POST.getlist('images[]')
    body = request.POST.get('body')
    thread_id = request.POST.get('thread')
    print(thread_id)
    oPost = models.Post(user_id=currentUid,body=body, thread_id=thread_id)
    oPost.save()
    if images:
        i = 1
        for image in images:
            imageArr = image.split(',')
            file_name = 'image_' + str(oPost.id) + '_' + str(i) + '.png'
            fh = open(constants['UPLOADS_DIRECTORY'] + "post_images/" + file_name, "wb")
            fh.write(imageArr[1].decode('base64'))
            fh.close()
            oPostImage = models.PostImage(post=oPost,image_name=file_name,order=i)
            oPostImage.save()
            i = i + 1
    response = oPost.objectify(currentUid)
    return HttpResponse(json.dumps(response), content_type = "application/json")

@csrf_exempt
def new_comment(request):
    post_id = int( request.POST.get('post_id') )
    uid = int( request.POST.get('uid') )
    body = request.POST.get('body')
    oComment = models.PostComment(user_id=uid,body=body,post_id=post_id)
    oComment.save()
    response = oComment.objectify(uid)
    return HttpResponse(json.dumps(response), content_type = "application/json")


@csrf_exempt
def edit_post(request):
    post_id = int( request.POST.get('post_id') )
    body = request.POST.get('body')
    oPost = models.Post.objects.all().get(id=post_id)
    oPost.body = body
    oPost.save()
    response = oPost.objectify(oPost.user.id)
    return HttpResponse(json.dumps(response), content_type = "application/json")

@csrf_exempt
def delete_post(request):
    post_id = int( request.POST.get('post_id') )
    oPost = models.Post.objects.all().get(id=post_id)
    oPost.delete()
    response = {
        'postId' : post_id        
    }
    if 'redirect' in request.POST:
        dest = request.POST.get('redirect')
        messages.success(request, 'Event successfully deleted.')
        return redirect(dest)
    return HttpResponse(json.dumps(response), content_type = "application/json")


@csrf_exempt
def edit_comment(request):
    comment_id = int( request.POST.get('comment_id') )
    body = request.POST.get('body')
    oComment = models.PostComment.objects.all().get(id=comment_id)
    oComment.body = body
    oComment.save()
    response = oComment.objectify(oComment.user.id)
    return HttpResponse(json.dumps(response), content_type = "application/json")

@csrf_exempt
def delete_comment(request):
    comment_id = int( request.POST.get('comment_id') )
    oComment = models.PostComment.objects.all().get(id=comment_id)
    oComment.delete()
    response = {
        'commentId' : comment_id        
    }
    return HttpResponse(json.dumps(response), content_type = "application/json")












