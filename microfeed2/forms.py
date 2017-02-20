import random, string

from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field

from microfeed2 import models
from images.helpers import parse_image_str


def get_post_form(form_type="general"):
    
    
    
    if form_type == "event":
        class PostForm(forms.ModelForm):
            images = forms.CharField(widget=forms.HiddenInput, required=False)
            start_date = forms.DateField(widget=forms.DateInput, required=True, input_formats=['%Y-%m-%d',      # '2006-10-25'
                                                                                            '%m/%d/%Y',      # '10/25/2006'
                                                                                            '%m/%d/%y',      # '10/25/06''%b %d %Y',      # 'Oct 25 2006'
                                                                                            '%b %d, %Y',     # 'Oct 25, 2006'
                                                                                            '%d %b %Y',      # '25 Oct 2006'
                                                                                            '%d %b, %Y',     # '25 Oct, 2006'
                                                                                            '%B %d %Y',      # 'October 25 2006'
                                                                                            '%B %d, %Y',     # 'October 25, 2006'
                                                                                            '%d %B %Y',      # '25 October 2006'
                                                                                            '%d %B, %Y']     # '25 October, 2006')
            )
            start_time = forms.TimeField(widget=forms.TimeInput, required=True, input_formats=['%I:%M %p'],)
            end_time = forms.TimeField(widget=forms.TimeInput, required=False, input_formats=['%I:%M %p'],)
            
            class Meta:
                model = models.Post
                fields = ['title', 'body', 'thread', 'type']
                widgets = {
                  'body' : forms.Textarea(attrs={'rows':4, 'cols':30}),
                  'thread' : forms.HiddenInput(),
                  'type' : forms.HiddenInput(),
                }
                labels = {
                  'body': '',
                  'title' : ''
                }
                
            def __init__(self, *args, **kwargs):
                oPost = kwargs.get('instance', None)
                if oPost:
                    css_id  = 'id_images-' + str(oPost.id)
                else:
                    css_id = 'id_images-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
                self.helper = FormHelper()
                self.helper.form_tag = False
                self.helper.layout = Layout(
                    'type',
                    'thread',
                    Field('title',
                        placeholder = 'Event title'
                    ),
                    Field('body',
                        placeholder = 'Description...'
                    ),
                    HTML('<div class="row">'),
                        HTML('<div class="col-sm-4">'),
                            'start_date',
                        HTML('</div>'),
                        HTML('<div class="col-sm-4">'),
                            'start_time',
                        HTML('</div>'),
                        HTML('<div class="col-sm-4">'),
                            'end_time',
                        HTML('</div>'),
                    HTML('</div>'),
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
                self.fields['type'].initial = form_type
                
                if oPost:
                    qStartTime = oPost.posttime_set.all()
                    self.fields['start_date'].initial = qStartTime[0].start_date
                    self.fields['start_time'].initial = qStartTime[0].start_time
                    self.fields['end_time'].initial = qStartTime[0].end_time
                    qPostImages = oPost.postimage_set.all()
                    images_str = ''
                    for oPostImage in qPostImages:
                        images_str = images_str + oPostImage.image_name + ','
                    self.fields['images'].initial = images_str
                
            def save(self, user):
                oPost = super(PostForm, self).save(commit=False)
                oPost.user = user
                oPost.save()
                # update date and time
                qPostTime = models.PostTime.objects.all().filter(post=oPost)
                for oPostTime in qPostTime:
                    oPostTime.delete()
                start_date = self.cleaned_data['start_date']
                start_time = self.cleaned_data['start_time']
                end_time = self.cleaned_data.get('end_time', None)
                oPostTime = models.PostTime(post=oPost, start_date=start_date, start_time=start_time, end_time=end_time)
                oPostTime.save()
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
            
        return PostForm
    
    #########################################################
    if form_type == 'classified':
        title_placeholder = _('Classified ad title')
        placeholder = _('Details...')
    else:
        title_placeholder = ''
        placeholder = _('Write a general message...')
        

    class PostForm(forms.ModelForm):
        images = forms.CharField(widget=forms.HiddenInput, required=False)
        form_type = forms.CharField(widget=forms.HiddenInput, required=False)
        
        class Meta:
            model = models.Post
            if form_type == 'classified':
                fields = ['title', 'body', 'thread', 'type']
            else:
                fields = ['body', 'thread', 'type']
            widgets = {
              'body' : forms.Textarea(attrs={'rows':4, 'cols':30}),
              'thread' : forms.HiddenInput(),
              'type' : forms.HiddenInput(),
            }
            labels = {
              'body': '',
              'title' : ''
            }
            
        def __init__(self, *args, **kwargs):
            oPost = kwargs.get('instance', None)
            if oPost:
                css_id  = 'id_images-' + str(oPost.id)
            else:
                css_id = 'id_images-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
            self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.layout = Layout(
                'type',
                'thread',
                Field('title',
                    placeholder = title_placeholder
                ),
                Field('body',
                    placeholder = placeholder
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
            self.fields['type'].initial = form_type
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
        
    return PostForm

        
    
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
                placeholder = _('Add a comment...')   
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
