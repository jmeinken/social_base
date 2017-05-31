import random
import string
import json

from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field 
from crispy_forms.bootstrap import PrependedText


from . import models
from microfeed2.models import PostThread
from field_trans.helpers import set_translation
from field_trans.models import Translation

languages = [
    'Japanese',
    'German',
    'Chinese',
]



class PageForm(forms.Form):
    qCategory = models.PageCategory.objects.all().filter(parent=None)
    CATEGORY_CHOICES = []
    for oCategory in qCategory:
        choice = (oCategory.id, oCategory.title,)
        CATEGORY_CHOICES.append(choice)
        
    category = forms.ChoiceField(label=_('CATEGORY'), choices=CATEGORY_CHOICES)
    title = forms.CharField(label='', required=False)
    title_japanese = forms.CharField(label='', required=False)
    title_german = forms.CharField(label='', required=False)
    body = forms.CharField(widget=forms.Textarea, label='', required=False)
    body_japanese = forms.CharField(widget=forms.Textarea, label='', required=False)
    body_german = forms.CharField(widget=forms.Textarea, label='', required=False)
    address = forms.CharField(label=_('ADDRESS'), required=False)
    contact_email = forms.CharField(label=_('CONTACT EMAIL'), required=False)
    image = forms.CharField(widget=forms.HiddenInput, required=False)
    url1 = forms.URLField(label=_('URL'), required=False)
    url1_label = forms.CharField(label='', required=False)
    url1_label_japanese = forms.CharField(label='', required=False)
    url1_label_german = forms.CharField(label='', required=False)
    url2 = forms.URLField(label=_('URL'), required=False)
    url2_label = forms.CharField(label='', required=False)
    url2_label_japanese = forms.CharField(label='', required=False)
    url2_label_german = forms.CharField(label='', required=False)
    url3 = forms.URLField(label=_('URL'), required=False)
    url3_label = forms.CharField(label='', required=False)
    url3_label_japanese = forms.CharField(label='', required=False)
    url3_label_german = forms.CharField(label='', required=False)

    def __init__(self, *args, **kwargs):
        # build template
        self.template = FormHelper()
        self.template.form_tag = False            # don't attach <form> tag
        self.template.disable_csrf = True        # don't auto-add csrf token
        self.template.layout = get_page_layout()
        # call super
        super(PageForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        data = super(PageForm, self).clean()
        if not data['title'] and not data['title_japanese'] and not data['title_german']:
            self.add_error('title', _("Please enter a title for at least 1 language."))
            self.add_error('title_japanese', _("Please enter a title for at least 1 language."))
            self.add_error('title_german', _("Please enter a title for at least 1 language."))
        if not data['body'] and not data['body_japanese'] and not data['body_german']:
            self.add_error('body', _("Please enter a body for at least 1 language."))
            self.add_error('body_japanese', _("Please enter a body for at least 1 language."))
            self.add_error('body_german', _("Please enter a body for at least 1 language."))
        if data['url1_label'] or data['url1_label_japanese'] or data['url1_label_german']:
            if not data['url1']:
                self.add_error('url1', _('You must have a link URL if you specify a link name.'))
        if data['url2_label'] or data['url2_label_japanese'] or data['url2_label_german']:
            if not data['url2']:
                self.add_error('url2', _('You must have a link URL if you specify a link name.'))
        if data['url3_label'] or data['url3_label_japanese'] or data['url3_label_german']:
            if not data['url3']:
                self.add_error('url3', _('You must have a link URL if you specify a link name.'))
                
        
        
    def set_edit_page(self, oPage):
        self.fields['category'].initial = oPage.category.id
        self.fields['title'].initial = oPage.title
        title_trans = oPage.all_trans_title()
        if 'ja' in title_trans:
            self.fields['title_japanese'].initial = title_trans['ja']
        if 'de' in title_trans:
            self.fields['title_german'].initial = title_trans['de']
        self.fields['body'].initial = oPage.body
        body_trans = oPage.all_trans_body()
        if 'ja' in body_trans:
            self.fields['body_japanese'].initial = body_trans['ja']
        if 'de' in body_trans:
            self.fields['body_german'].initial = body_trans['de']
        self.fields['address'].initial = oPage.address
        self.fields['contact_email'].initial = oPage.contact_email
        self.fields['image'].initial = oPage.image
        qLink = oPage.pagelink_set.all()
        if qLink.count() >= 1:
            self.fields['url1'].initial = qLink[0].url
            self.fields['url1_label'].initial = qLink[0].title
            title_trans = qLink[0].all_trans_title()
            if 'ja' in title_trans:
                self.fields['url1_label_japanese'].initial = title_trans['ja']
            if 'de' in title_trans:
                self.fields['url1_label_german'].initial = title_trans['de']
        if qLink.count() >= 2:
            self.fields['url2'].initial = qLink[1].url
            self.fields['url2_label'].initial = qLink[1].title
            title_trans = qLink[1].all_trans_title()
            if 'ja' in title_trans:
                self.fields['url2_label_japanese'].initial = title_trans['ja']
            if 'de' in title_trans:
                self.fields['url2_label_german'].initial = title_trans['de']
        if qLink.count() >= 3:
            self.fields['url3'].initial = qLink[2].url
            self.fields['url3_label'].initial = qLink[2].title
            title_trans = qLink[2].all_trans_title()
            if 'ja' in title_trans:
                self.fields['url3_label_japanese'].initial = title_trans['ja']
            if 'de' in title_trans:
                self.fields['url3_label_german'].initial = title_trans['de']
            
    def save_page(self, user, oPage=None):
        data = self.cleaned_data
        if oPage:
            # delete translations
            Translation.objects.filter(
                table_name='Page',
                field_id=oPage.id
            ).delete()
            # delete pagelink translations
            for oPageLink in oPage.pagelink_set.all():
                Translation.objects.filter(
                    table_name='PageLink',
                    field_id=oPageLink.id
                ).delete()
            # delete pagelink
            oPage.pagelink_set.all().delete()
            # save changes to oPage
            oPage.category_id = data['category']
            oPage.title = data['title']
            oPage.body = data['body']
            oPage.address = data['address']
            oPage.contact_email = data['contact_email']
            oPage.image = data['image']
            oPage.last_edited_by = user
            oPage.save()
        else:
            # create a comment thread
            oPostThread = PostThread(title=data['title'])
            oPostThread.allow_comments = False
            oPostThread.save()
            # create a page
            oPage = models.Page(
                category_id=data['category'],
                title=data['title'],
                body=data['body'],
                address=data['address'],
                contact_email=data['contact_email'],
                image=data['image'],
                language_id='en',
                created_by=user,
                last_edited_by=user,               
            )
            oPage.save()
        # save all translations
        if data['title_japanese']:
            set_translation('Page', 'title', oPage.id, 'ja', data['title_japanese'])
        if data['body_japanese']:
            set_translation('Page', 'body', oPage.id, 'ja', data['body_japanese'])
        # save links
        if data['url1']:
            oLink1 = models.PageLink(
                page = oPage,
                title =  data['url1_label'],
                url = data['url1'],
                order = 1
            )
            oLink1.save()
            if data['url1_label_japanese']:
                set_translation('PageLink', 'title', oLink1.id, 'ja', data['url1_label_japanese'])
        if data['url2']:
            oLink2 = models.PageLink(
                page = oPage,
                title =  data['url2_label'],
                url = data['url2'],
                order = 2
            )
            oLink2.save()
            if data['url2_label_japanese']:
                set_translation('PageLink', 'title', oLink2.id, 'ja', data['url2_label_japanese'])
        if data['url3']:
            oLink3 = models.PageLink(
                page = oPage,
                title =  data['url3_label'],
                url = data['url3'],
                order = 3
            )
            oLink3.save()
            if data['url3_label_japanese']:
                set_translation('PageLink', 'title', oLink3.id, 'ja', data['url3_label_japanese'])
        # save page history
        json_data = json.dumps(data)
        oPageHistory = models.PageHistory(
             page = oPage,
             user = user,
             data = json_data       
        )
        oPageHistory.save()
        # return oPage
        return oPage
        
        
        
        
        
        
        


def get_page_layout():
    code = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
    
    page_title_generic_selector = '''
        <ul class="nav nav-pills" style="padding:5px;">
            <li class="active">
                <a href="#[*]_english_tab" data-toggle="tab">
                    ''' + __('English') + ''' <span class="language-input-status" data-tab="[*]_english_tab"></span>
                </a>
            </li>
            <li>
                <a href="#[*]_japanese_tab" data-toggle="tab">
                    ''' +  __('Japanese') + ''' <span class="language-input-status" data-tab="[*]_japanese_tab"></span>
                </a>
            </li>
            <li>
                <a href="#[*]_german_tab" data-toggle="tab">
                    ''' + __('German') + ''' <span class="language-input-status" data-tab="[*]_german_tab"></span>
                </a>
            </li>
        </ul>
    '''
    
    PAGE_TITLE_LANGUAGE_SELECTOR = page_title_generic_selector.replace('[*]', 'title_' + code)
    PAGE_BODY_LANGUAGE_SELECTOR = page_title_generic_selector.replace('[*]', 'body_' + code)
    PAGE_URL1_TITLE_LANGUAGE_SELECTOR = page_title_generic_selector.replace('[*]', 'url1_label_' + code)
    PAGE_URL2_TITLE_LANGUAGE_SELECTOR = page_title_generic_selector.replace('[*]', 'url2_label_' + code)
    PAGE_URL3_TITLE_LANGUAGE_SELECTOR = page_title_generic_selector.replace('[*]', 'url3_label_' + code)
    
    
    page_layout = Layout(
        Div('category', css_class = 'well well-sm'),
        Div(    
            HTML(_('TITLE') + '*'),   
            HTML(PAGE_TITLE_LANGUAGE_SELECTOR),  
            Div(         
                Div('title', css_class='tab-pane fade active in', css_id='title_' + code + '_english_tab'),
                Div('title_german', css_class='tab-pane fade', css_id='title_' + code + '_german_tab'),
                Div('title_japanese', css_class='tab-pane fade', css_id='title_' + code + '_japanese_tab'),
                css_class='tab-content'
            ),
            css_class = 'well well-sm'
        ),
        Div(    
            HTML(_('BODY') + '*'),   
            HTML(PAGE_BODY_LANGUAGE_SELECTOR),  
            Div(         
                Div('body', css_class='tab-pane fade active in add-tinymce', css_id='body_' + code + '_english_tab'),
                Div('body_german', css_class='tab-pane fade add-tinymce', css_id='body_' + code + '_german_tab'),
                Div('body_japanese', css_class='tab-pane fade add-tinymce', css_id='body_' + code + '_japanese_tab'),
                css_class='tab-content'
            ),
            css_class = 'well well-sm'
        ),
        Div(
            Field('image', 
                css_class = 'image_input', 
                data_label = _('PAGE IMAGE'),
                data_export_zoom = 2,
                data_min_zoom = 'fill',
                data_aspect_ratio = '2:1',
                id = 'image_' + code
            ),
            css_class = 'well well-sm'
        ),
        Div('address', css_class = 'well well-sm'),
        Div('contact_email', css_class = 'well well-sm'),
        Div(    
            HTML(_('LINK 1 NAME')),   
            HTML(PAGE_URL1_TITLE_LANGUAGE_SELECTOR),  
            Div(         
                Div('url1_label', css_class='tab-pane fade active in', css_id='url1_label_' + code + '_english_tab'),
                Div('url1_label_japanese', css_class='tab-pane fade', css_id='url1_label_' + code + '_japanese_tab'),
                Div('url1_label_german', css_class='tab-pane fade', css_id='url1_label_' + code + '_german_tab'),
                css_class='tab-content'
            ),
            'url1',
            css_class = 'well well-sm'
        ),
        Div(    
            HTML(_('LINK 2 NAME')),   
            HTML(PAGE_URL2_TITLE_LANGUAGE_SELECTOR),  
            Div(         
                Div('url2_label', css_class='tab-pane fade active in', css_id='url2_label_' + code + '_english_tab'),
                Div('url2_label_japanese', css_class='tab-pane fade', css_id='url2_label_' + code + '_japanese_tab'),
                Div('url2_label_german', css_class='tab-pane fade', css_id='url2_label_' + code + '_german_tab'),
                css_class='tab-content'
            ),
            'url2',
            css_class = 'well well-sm'
        ),
        Div(    
            HTML(_('LINK 3 NAME')),   
            HTML(PAGE_URL3_TITLE_LANGUAGE_SELECTOR),  
            Div(         
                Div('url3_label', css_class='tab-pane fade active in', css_id='url3_label_' + code + '_english_tab'),
                Div('url3_label_japanese', css_class='tab-pane fade', css_id='url3_label_' + code + '_japanese_tab'),
                Div('url3_label_german', css_class='tab-pane fade', css_id='url3_label_' + code + '_german_tab'),
                css_class='tab-content'
            ),
            'url3',
            css_class = 'well well-sm'
        ),
    )
    return page_layout


### OLD #########################################################################



class TranslateForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput)
    body = forms.CharField(widget=forms.TextInput)
    teaser = forms.CharField(widget=forms.TextInput)


class OldPageForm(forms.ModelForm):
    class Meta:
        model = models.Page
        fields = ['language', 'order', 'category','title','body','teaser','address','image']
        widgets = {
          'body': forms.Textarea(attrs={'rows':25, 'cols':30}),
          'image': forms.HiddenInput()
        }
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.disable_csrf = True
        self.helper.layout = Layout(
                HTML('<div class="row"><div class="col-sm-4">'),
                'language',
                'category',
                'title',
                'order',
                'address',
                Field('image', 
                    css_class = 'image_input', 
                    data_label = 'Page Image',
                    data_export_zoom = 2,
                    data_min_zoom = 'fill',
                    data_aspect_ratio = '2:1'
                ),
                HTML('</div><div class="col-sm-8">'),
                'teaser',
                'body',
                HTML('</div></div>')
                
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
        fields = ['parent', 'language', 'title','order', 'show_as_page']
    
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