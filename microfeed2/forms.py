from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field

from microfeed import models
from images.helpers import parse_image_str



class PostForm(forms.ModelForm):
    images = forms.CharField(widget=forms.HiddenInput, required=False)
    
    class Meta:
        model = models.Post
        fields = ['body', 'thread']
        widgets = {
          'body' : forms.Textarea(attrs={'rows':4, 'cols':30}),
          'thread' : forms.HiddenInput()
        }
        labels = {
          'body': '',
        }
        
    def __init__(self, *args, **kwargs):
        print(kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.disable_csrf = True
        oPost = kwargs.get('instance', None)
        if oPost:
            css_id  = 'id_images-' + str(oPost.id)
        else:
            css_id = 'id_images'
        self.helper.layout = Layout(
            'thread',
            Field('body',
                placeholder = 'Write a general message...'   
            ),
            Field('images', 
                id = css_id,
                css_class = 'image_input',             # tells JS crp tool that this is a crop-it image input
                data_multiple_allowed = 'yes',        # 
                data_label = '',            # give human readable title for image
                data_export_zoom = 2,                # set crop-it zoom over original size
                data_min_zoom = 'fill',                # set min zoom to fill or fit
                data_aspect_ratio = '4:3',            # currently supported are 1:1 and 4:3
                data_base_name = 'post_image'           # the name that will be used to generate image name (image number and '.png' will be appended
            ),
        )
        super(PostForm, self).__init__(*args, **kwargs)
        if oPost:
            qPostImages = oPost.postimage_set.all()
            images_str = ''
            for oPostImage in qPostImages:
                images_str = images_str + oPostImage.image_name + ','
            self.fields['images'].initial = images_str
        
    def save(self, user):
        oPost = super(PostForm, self).save(commit=False)
        oPost.user = user
        oPost.save()
        # remove previous images on oPost
        qPostImage = models.PostImage.objects.all().filter(post=oPost)
        for oPostImage in qPostImage:
            oPostImage.delete()
        # add images from form to oPost
        image_str = self.cleaned_data['images']
        print(parse_image_str(image_str))
        images = parse_image_str(image_str)
        i = 1
        for image in images:
            oPostImage = models.PostImage(post=oPost, image_name=image, order=i)
            oPostImage.save()
            i = i + 1
        return oPost
    
    
class PostCommentForm(forms.ModelForm):
    
    class Meta:
        model = models.PostComment
        fields = ['body']
        widgets = {
          'body': forms.Textarea(attrs={'rows':1, 'cols':30}),
        }
        labels = {
          'body': '',
        }
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Field('body',
                placeholder = 'Add a comment...'   
            ),
        )
        super(PostCommentForm, self).__init__(*args, **kwargs)
        
    def save(self, user=None, post_id=None):
        oPostComment = super(PostCommentForm, self).save(commit=False)
        if user:
            oPostComment.user = user
        if post_id:
            oPostComment.post_id = post_id
        oPostComment.save()
        return oPostComment
