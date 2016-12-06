from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.shortcuts import reverse

from email_handler.helpers import send_system_mail
from main.helpers import constants




class AccountEditForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.disable_csrf = True
        self.helper.layout = Layout(
                # 'id',
                'username',
                'email',
                Field('image', 
                    css_class = 'image_input', 
                    data_label = 'User Image',
                    data_export_zoom = 2,
                    data_min_zoom = 'fill',
                    data_aspect_ratio = '1:1'
                ),
        )
        super(AccountEditForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance', None):
            self.editing_existing = True
        else:
            self.editing_existing = False
    
    def clean(self):
        cleaned_data = super(AccountEditForm, self).clean()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email','image']
        widgets = {
            'image' : forms.HiddenInput
        }
        
    def save(self):
        user = self.instance
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.image = self.cleaned_data['image']
        user.save()
        
class ForgotPasswordForm(forms.Form):
    username_or_email = forms.CharField(max_length=50, widget=forms.TextInput, required=True, label='enter your username or email address')
    
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.disable_csrf = True
        self.helper.layout = Layout(
                # 'id',
                'username_or_email',
        )
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance', None):
            self.editing_existing = True
        else:
            self.editing_existing = False
    
    def clean(self):
        cleaned_data = super(ForgotPasswordForm, self).clean()
        id = cleaned_data.get('username_or_email')
        User = get_user_model()
        qUser = User.objects.all().filter(username=id)
        if not qUser:
            qUser = User.objects.all().filter(email=id)
        if not qUser:
            self.add_error('username_or_email', 'That username or email address wasn\'t found in our system.')

    def email_forgot_password(self, request):
        id = self.cleaned_data.get('username_or_email')
        User = get_user_model()
        qUser = User.objects.all().filter(username=id)
        if not qUser:
            qUser = User.objects.all().filter(email=id)
        oUser = qUser[0]
        oUser.create_temp_code()
        oUser.save()
        print('email forgot password to ' + oUser.username)
        body = '''Use the following link to reset your password.'''
        email_context = {
            'name' : oUser.get_short_name(),
            'body' : body,                        # plain text (no html), line breaks will be converted to <br> in html version
            'subject' : 'password reset',
            'link' : constants['BASE_URL'] + reverse('reset_password', args={oUser.temp_code}),
            'unsubscribe_code' : oUser.perma_code             
        }
        message = render_to_string('email_handler/email_generic.txt', email_context, request)
        html_message = render_to_string('email_handler/email_generic.html', email_context, request)
        send_system_mail(
            subject = 'password reset',
            message = message,
            html_message = html_message,
            from_mail = constants['CONTACT_EMAIL'],
            to_list = [oUser.email]                     
        )
    

       
        
class CreateAccountForm(forms.ModelForm):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True, label='Password', help_text='Minimum 8 characters.')
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True, label='Reenter Password')
    # image = forms.CharField(max_length=255, widget=forms.HiddenInput, required=False)
    # image2 = forms.CharField(max_length=255, widget=forms.HiddenInput, required=False)
    # image_set = forms.CharField(max_length=255, widget=forms.HiddenInput, required=False)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.disable_csrf = True
        self.helper.layout = Layout(
                # 'id',
                'username',
                'email',
                Field('image', 
                    css_class = 'image_input', 
                    data_label = 'User Image',
                    data_export_zoom = 2,
                    data_min_zoom = 'fill',
                    data_aspect_ratio = '1:1'
                ),
                'password1',
                'password2',  
        )
        super(CreateAccountForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance', None):
            self.editing_existing = True
        else:
            self.editing_existing = False
    
    def clean(self):
        cleaned_data = super(CreateAccountForm, self).clean()
        pw1 = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")
        if not pw1 and not self.editing_existing:
            self.add_error('password1', 'A password is required.')
        if pw1:
            if len(pw1) < 8:
                self.add_error('password1', 'Password must be at least 8 characters.')
            if pw1 != pw2:
                self.add_error('password2', 'Password values didn\'t match.')

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'image']
        widgets = {
            'image' : forms.HiddenInput
        }
        
    def save(self):
        user = get_user_model().objects.create_user(self.cleaned_data['username'],
                                  self.cleaned_data['email'],
                                  self.cleaned_data['password1'])
        user.image = self.cleaned_data['image']
        user.save()
        return user
        
        
class PasswordForm(forms.ModelForm):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput, required=False, label='Password', help_text='Minimum 8 characters.')
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput, required=False, label='Reenter Password')
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.disable_csrf = True
        self.helper.layout = Layout(
                # 'id',
                'password1',
                'password2',
        )
        super(PasswordForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        pw1 = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")
        if not pw1 and not self.instance:
            self.add_error('password1', 'A password is required.')
        if pw1:
            if len(pw1) < 8:
                self.add_error('password1', 'Password must be at least 8 characters.')
            if pw1 != pw2:
                self.add_error('password2', 'Password values didn\'t match.')

    class Meta:
        model = get_user_model()
        fields = []
        
    def save(self):
        user = self.instance
        user.set_password( self.cleaned_data['password1'] )
        user.save()
        return user
        
        
        
        
        