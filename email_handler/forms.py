from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field

from django.contrib.auth import get_user_model




class ComposeEmailForm(forms.Form):
    user = forms.ModelChoiceField(
            get_user_model().objects.all().exclude(email__isnull=True).exclude(email=''),
            empty_label="--select--", 
            required=True)
    subject = forms.CharField(max_length=120, required=True)
    body = forms.CharField(max_length=1000, required=True, widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.disable_csrf = True
        self.helper.layout = Layout(
                # 'id',
                'user',
                'subject',
                'body',
        )
        super(ComposeEmailForm, self).__init__(*args, **kwargs)