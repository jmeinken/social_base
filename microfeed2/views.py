from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from . import forms
from microfeed import models




@login_required
def home(request):
    context = {}
    context['fPost'] = forms.PostForm()
    return render(request, 'microfeed2/home.html', context)

@login_required
def home2(request):
    context = {}
    context['fPost'] = forms.PostForm()
    context['callback'] = reverse('microfeed2:new_post')
    return render(request, 'microfeed2/home2.html', context)


def view_post(request, post_id):
    context = {}        # context for rendering views
    response = {}       # json response object
    oPost = models.Post.objects.get(pk=post_id)
    context['oPost'] = oPost
    
    if request.is_ajax():
        response['html'] = render_to_string('microfeed2/blocks/post.html', context, request)
        response['destinationId'] = 'mf-post-' + str(post_id)
        return JsonResponse(response, safe=False)
    else:
        return render(request, 'microfeed2/view_post.html', context)

@login_required
def new_post(request):
    context = {}        # context for rendering views
    response = {}       # json response object
    
    ### return blank form if not post ###
    if not request.POST:
        # set up context
        context['fPost'] = forms.PostForm()
        context['callback'] = reverse('microfeed2:new_post')
        if request.is_ajax():
            response['html'] = render_to_string('microfeed2/blocks/post_form.html', context, request)
            return JsonResponse(response, safe=False)
        else:
            return render(request, 'microfeed2/new_post.html', context)
        
    ### return form with errors or confirmation
    else:
        fPost = forms.PostForm(request.POST)
        
        ### return confirmation
        if fPost.is_valid():
            oPost = fPost.save(request.user)
            if request.is_ajax():
                context['oPost'] = oPost
                context['fPostComment'] = forms.PostCommentForm()
                response['html'] = render_to_string('microfeed2/blocks/post_block.html', context, request)
                response['status'] = 'Successfully created post.'
                return JsonResponse(response, safe=False)
            else:
                messages.success(request, 'Successfully created post.')
                return redirect('home')
            
        ### return form with errors
        else:
            context['form'] = fPost
            if request.is_ajax():
                context['callback'] = reverse('microfeed2:new_post')
                response['html'] = render_to_string('microfeed2/blocks/post_form.html', context, request)
                return JsonResponse(response, safe=False)
            else:
                return render(request, 'microfeed2/new_post.html', context)

@login_required
def edit_post(request, post_id):
    context = {}        # context for rendering views
    response = {}       # json response object
    oPost = models.Post.objects.get(pk=post_id)
    
    ### return blank form if not post ###
    if not request.POST:
        # set up context
        context['fPost'] = forms.PostForm(instance=oPost)
        context['callback'] = reverse('microfeed2:edit_post', args=[post_id])
        context['oPost'] = oPost
        if request.is_ajax():
            response['html'] = render_to_string('microfeed2/blocks/edit_post_form.html', context, request)
            response['destinationId'] = 'mf-post-' + str(post_id)
            return JsonResponse(response, safe=False)
        else:
            return render(request, 'microfeed2/edit_post.html', context)
        
    ### return form with errors or confirmation
    else:
        fPost = forms.PostForm(request.POST, instance=oPost)
        
        ### return confirmation
        if fPost.is_valid():
            oPost = fPost.save(request.user)
            if request.is_ajax():
                context['oPost'] = oPost
                response['html'] = render_to_string('microfeed2/blocks/post.html', context, request)
                response['message'] = 'Successfully edited post.'
                response['status'] = 'success'
                response['destinationId'] = 'mf-post-' + str(post_id)
                return JsonResponse(response, safe=False)
            else:
                messages.success(request, 'Successfully edited post.')
                return redirect('home')
            
        ### return form with errors
        else:
            context['form'] = fPost
            context['callback'] = reverse('microfeed2:edit_post', args=[post_id])
            if request.is_ajax():
                response['html'] = render_to_string('microfeed2/blocks/edit_post_form.html', context, request)
                response['status'] = 'form errors'
                return JsonResponse(response, safe=False)
            else:
                return render(request, 'microfeed2/edit_post.html', context)
            
@login_required
@csrf_exempt
def delete_post(request, post_id):
    context = {}        # context for rendering views
    response = {}       # json response object
    
    if request.POST:        # nothing actually needs to be sent in the post, just used to prevent accidental deleting
        oPost = models.Post.objects.get(pk=post_id)
        oPost.delete()
        if request.is_ajax():
            context['message'] = 'Post successfully deleted.'
            response['html'] = render_to_string('microfeed2/snippets/delete_confirmation.html', context, request)
            response['status'] = 'success'
            response['destinationId'] = 'mf-post-block-' + str(post_id)
            return JsonResponse(response, safe=False)
        else:
            messages.success(request, 'Successfully deleted.')
            return redirect('home')
    else:
        return redirect('home')












def ajax_posts(request):
    '''Returns the html for a collection of posts.
    '''
    last_post_id = int( request.GET.get('last_post_id', 1000000) )
    thread_id = int( request.GET.get('thread_id', 1) )
    qPost = models.Post.objects.filter(thread_id=thread_id).filter(id__lt=last_post_id)[:3]
    # attach forms where appropriate
    fPostComment = forms.PostCommentForm()
    context = {  
       'qPost' : qPost, 
       'fPostComment' : fPostComment,
       'last_post_id' : last_post_id
    }
    html = render_to_string('microfeed2/blocks/feed.html', context, request)
    response = {}
    response['html'] = html
    modals = render_to_string('microfeed2/blocks/feed_modals.html', {}, request)
    response['modals'] = modals
    if qPost:
        for oPost in qPost:
            response['lastPostId'] = oPost.id
        response['status'] = 'unfinished'
    else:
        response['status'] = 'finished'
    return JsonResponse(response, safe=False)

@login_required
def ajax_edit_post(request, post_id):
    context = {}
    print(post_id)
    oPost = models.Post.objects.all().get(pk=post_id)
    form = forms.PostForm(instance=oPost)
    if request.POST:
        form = forms.PostForm(request.POST, instance=oPost)
        if form.is_valid():
            oPost = form.save(request.user)
    oPost.fPost = form
    context['oPost'] = oPost
    html = render_to_string('microfeed2/blocks/post.html', context, request)
    response = {}
    response['html'] = html
    response['destinationId'] = 'mf-post-' + str(post_id)
    return JsonResponse(response, safe=False)

@login_required
def ajax_new_comment(request, post_id):
    context = {}
    response = {}
    fComment = forms.PostCommentForm()
    if request.POST:
        fComment = forms.PostCommentForm(request.POST)
        if fComment.is_valid():
            oComment = fComment.save(request.user, post_id)
            context['oComment'] = oComment
            response['status'] = 'complete'
            response['html'] = render_to_string('microfeed2/blocks/comment.html', context, request)
            response['postId'] = post_id
            return JsonResponse(response, safe=False)
        else:
            response['status'] = 'incomplete'
    context['fComment'] = fComment
    html = render_to_string('microfeed2/blocks/comment_form.html', context, request)
    response['html'] = html
    response['postId'] = post_id
    return JsonResponse(response, safe=False)

@login_required
def ajax_edit_comment(request, comment_id):
    context = {}
    response = {}
    oComment = models.PostComment.objects.all().get(pk=comment_id)
    fComment = forms.PostCommentForm(instance=oComment)
    if request.POST:
        fComment = forms.PostCommentForm(request.POST, instance=oComment)
        if fComment.is_valid():
            oComment = fComment.save()
            response['status'] = 'complete'
            context['oComment'] = oComment
            html = render_to_string('microfeed2/blocks/comment.html', context, request)
            response['html'] = html
            response['destinationId'] = 'mf-comment-' + str(comment_id)
            return JsonResponse(response, safe=False)
        else:
            response['status'] = 'incomplete'
    context['oComment'] = oComment
    context['fComment'] = fComment
    html = render_to_string('microfeed2/blocks/comment_form.html', context, request)
    response['html'] = html
    response['destinationId'] = 'mf-edit-comment-' + str(comment_id)
    return JsonResponse(response, safe=False)

@csrf_exempt
def ajax_delete_post(request, post_id):
    oPost = models.Post.objects.all().get(id=post_id)
    oPost.delete()
    context = {
       'message' : 'Post successfully deleted.'        
    }
    html = render_to_string('microfeed2/snippets/delete_confirmation.html', context, request)
    response = {
        'postId' : post_id,
        'html' : html,
        'destinationId' :  'mf-post-block-' + str(post_id)      
    }
    return JsonResponse(response, safe=False)

@csrf_exempt
def ajax_delete_comment(request, comment_id):
    oComment = models.PostComment.objects.all().get(id=comment_id)
    oComment.delete()
    context = {
       'message' : 'Comment successfully deleted.'        
    }
    html = render_to_string('microfeed2/snippets/delete_confirmation.html', context, request)
    response = {
        'commentId' : comment_id,
        'html' : html,
        'destinationId' : 'mf-comment-' + str(comment_id)
    }
    return JsonResponse(response, safe=False)








    