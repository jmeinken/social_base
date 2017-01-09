

from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field


from . import models
from microfeed.models import PostThread




class PageForm(forms.ModelForm):
    class Meta:
        model = models.Page
        fields = ['category','title','body','teaser','address','image']
        widgets = {
          'body': forms.Textarea(attrs={'rows':25, 'cols':30}),
          'image': forms.HiddenInput()
        }
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.disable_csrf = True
        self.helper.layout = Layout(
                # 'id',
                'category',
                'title',
                'body',
                'teaser',
                'address',
                Field('image', 
                    css_class = 'image_input', 
                    data_label = 'Page Image',
                    data_export_zoom = 2,
                    data_min_zoom = 'fill',
                    data_aspect_ratio = '2:1'
                ),
        )
        super(PageForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance', None):
            self.editing_existing = True
        else:
            self.editing_existing = False
    
    def save(self, commit=True):
        oPage = super(PageForm, self).save(commit=False)
        # create and attach a comment thread
        oPostThread = PostThread(title=oPage.title)
        oPostThread.allow_comments = False
        oPostThread.save()
        oPage.post_thread = oPostThread
        if commit:
            oPage.save()
        return oPage
       
        
 
        
class PageLinkForm(forms.ModelForm):
    title = 'Page Links'
    css_class = 'page-link-form'
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            HTML('<div class="' + self.css_class + ' row">'),
            'id',
            Div('title', css_class="col-sm-5"),
            Div('url', css_class="col-sm-5"),
            'DELETE',
            HTML('</div>')
        )
        super(PageLinkForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = models.PageLink
        fields = ['id', 'title', 'url']
        
PageLinkFormSet = inlineformset_factory( models.Page, models.PageLink, form=PageLinkForm, extra=2 )
PageLinkFormSet.title = _('Page Links')
PageLinkFormSet.css_class = 'page-link-form'


class PageCategoryForm(forms.ModelForm):
    class Meta:
        model = models.PageCategory
        fields = ['parent', 'title','show_as_page']
    
    def save(self, commit=True):
        oPageCategory = super(PageCategoryForm, self).save(commit=False)
        # create and attach a comment thread
        if oPageCategory.show_as_page:
            oPostThread = PostThread(title=oPageCategory.title)
            oPostThread.allow_comments = False
            oPostThread.save()
            oPageCategory.post_thread = oPostThread
        if commit:
            oPageCategory.save()
        return oPageCategory


#class PageImageForm(forms.ModelForm):
#    title = 'Page Images'
#    css_class = 'page-image-form'
#    
#    def __init__(self, *args, **kwargs):
#        self.helper = FormHelper()
#        self.helper.form_tag = False
#        self.helper.disable_csrf = True
#        self.helper.layout = Layout(
#            HTML('<div class="' + self.css_class + ' row">'),
#            'id',
#            Div('image_name', css_class="col-sm-3"),
#            Div('order', css_class="col-sm-3"),
#            'DELETE',
#            HTML('</div>')
#        )
#        super(PageImageForm, self).__init__(*args, **kwargs)
#    
#    class Meta:
#        model = models.PageImage
#        fields = ['id', 'image_name', 'order']
#        
#PageImageFormSet = inlineformset_factory( models.Page, models.PageImage, form=PageImageForm, extra=2 )
#PageImageFormSet.title = 'Page Images'
#PageImageFormSet.css_class = 'page-image-form'