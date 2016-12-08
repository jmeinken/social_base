from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML

from . import models



class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['body']
        widgets = {
          'body': forms.Textarea(attrs={'rows':10, 'cols':30}),
        }

class EventPostForm(forms.ModelForm):
    class Meta:
        model = models.EventPost
        fields = ['title']
        
class EventPostTimeForm(forms.ModelForm):
    css_class = 'time-form'
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            HTML('<div class="' + self.css_class + ' row">'),
                #'id',
                Div('start_date', css_class="col-sm-3"),
                Div('start_time', css_class="col-sm-3"),
                Div('end_time', css_class="col-sm-3"),
                'DELETE',
            HTML('</div>')
        )
        super(EventPostTimeForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = models.EventPostTime
        fields = ['event_post','start_date', 'start_time', 'end_time']

     
     
        
EventPostTimeFormSet = inlineformset_factory( models.EventPost, models.EventPostTime, form=EventPostTimeForm, extra=1 )
EventPostTimeFormSet.css_class = 'time-form'

        