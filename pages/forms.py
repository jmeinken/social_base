

from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML


from . import models




class PageForm(forms.ModelForm):
    class Meta:
        model = models.Page
        fields = ['category','title','body','teaser','address']
        widgets = {
          'body': forms.Textarea(attrs={'rows':25, 'cols':30}),
        }
 
        
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
            Div('title', css_class="col-sm-3"),
            Div('url', css_class="col-sm-3"),
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