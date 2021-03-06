from __future__ import unicode_literals

from django.shortcuts import reverse
from django.db import models
from django.conf import settings
from django.utils.timezone import localtime
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags

from field_trans.helpers import get_translation, get_translations

from microfeed2.models import PostThread
from field_trans.models import Language

from field_trans.models import Translation





class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        

# only show visible=True pages        
class ActivePageManager(models.Manager):
    def get_queryset(self):
        return super(ActivePageManager, self).get_queryset().filter(visible=True)
    


    

class PageCategory(TimeStampedModel):
    
   
    title             = models.CharField(max_length=255, verbose_name=_('title'),)
    language          = models.ForeignKey(Language)
    icon              = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('icon'),)
    parent            = models.ForeignKey("self", blank=True, null=True, related_name='child_set')
    show_as_page      = models.BooleanField(default=False)
    # add_microfeed     = models.BooleanField(default=False)
    post_thread       = models.ForeignKey(PostThread, blank=True, null=True, on_delete=models.SET_NULL)
    order             = models.IntegerField(default=0, verbose_name=_('order'),)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def trans_title(self):
        translation = get_translation('PageCategory', 'title', self.id)
        if translation:
            return translation
        else:
            return self.title
    
    def all_trans_title(self):
        return get_translations('PageCategory', 'title', self.id)
    
    def has_category_children(self):
        qChildren = self.child_set.all().filter(show_as_page=False)
        if qChildren:
            return True
        else:
            return False
        
    def get_hierarchy(self):
        current_object = self
        result = [self]
        while True:
            if current_object.parent:
                result.insert(0, current_object.parent)
                current_object = current_object.parent
            else:
                break
        return result
    
    def get_url(self):
        return reverse('pages:list', args=[self.id])
        
        
class Page(TimeStampedModel):
    title           = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('title'),)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL, related_name='created_page_set')
    last_edited_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL, related_name='last_edited_page_set')
    teaser          = models.TextField(blank=True, null=True, verbose_name=_('teaser'),)
    body            = models.TextField(blank=True, null=True, verbose_name=_('body'),)
    address         = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_('address'),)
    contact_email   = models.CharField(max_length=240, blank=True, null=True, verbose_name=_('contact email'),)
    order           = models.IntegerField(default=0, verbose_name=_('order'),)
    category        = models.ForeignKey('PageCategory', on_delete=models.PROTECT)
    visible         = models.BooleanField(default=True)
    post_thread     = models.ForeignKey(PostThread, blank=True, null=True, on_delete=models.SET_NULL)
    image           = models.CharField(max_length=30, blank=True, null=True)
    language        = models.ForeignKey(Language, on_delete=models.PROTECT)
    
    objects = models.Manager() # The default manager.
    visible_obj = ActivePageManager() # The only show visible manager.
    
    def __str__(self):
        return self.title
    
    def delete(self):
        # delete translations
        Translation.objects.filter(
            table_name='Page',
            field_id=self.id
        ).delete()
        for oPageLink in self.pagelink_set.all():
            Translation.objects.filter(
                table_name='PageLink',
                field_id=oPageLink.id
            ).delete()
        super(Page, self).delete()
    
    def get_url(self):
        return reverse('pages:view_page', args=[self.id])
    
    def get_hierarchy(self):
        category = self.category
        hierarchy = category.get_hierarchy()
        hierarchy.append(self)
        return hierarchy
    
    def trans_title(self):
        translation = get_translation('Page', 'title', self.id)
        if translation:
            return translation
        elif self.title:
            return self.title
        else:
            for lang, translation in get_translations('Page', 'title', self.id).items():
                if translation:
                    return translation
        return ''
        
    def trans_body(self):
        translation = get_translation('Page', 'body', self.id)
        if translation:
            return translation
        elif self.title:
            return self.body
        else:
            for lang, translation in get_translations('Page', 'body', self.id).items():
                if translation:
                    return translation
        return ''
        
    def trans_teaser(self):
        translation = get_translation('Page', 'body', self.id)
        if translation:
            return strip_tags(translation)[:400] + '...'
        elif self.title:
            return strip_tags(self.body)[:400] + '...'
        else:
            for lang, translation in get_translations('Page', 'body', self.id).items():
                if translation:
                    return strip_tags(translation)[:400] + '...'
        return ''
        
    def all_trans_title(self):
        return get_translations('Page', 'title', self.id)
    
    def all_trans_body(self):
        return get_translations('Page', 'body', self.id)
    
    def all_trans_teaser(self):
        return get_translations('Page', 'teaser', self.id)
        
    def get_image(self):
        if self.image:
            return 'uploads/' + self.image
        else:
            return ''
    
    class Meta:
        ordering = ['order', 'title']
        
        
# class PageImage(TimeStampedModel):
#     page        = models.ForeignKey("Page", on_delete=models.CASCADE)
#     # image       = models.ImageField(upload_to='page_images/', max_length=100)
#     order       = models.IntegerField(default=0)
#     
#     def get_image_path(self):
#         return self.image.url
#     
#     class Meta:
#         ordering = ['order', 'id']
        
class PageLink(TimeStampedModel):
    page        = models.ForeignKey("Page", on_delete=models.CASCADE)
    title       = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('title'),)
    url         = models.CharField(max_length=500, verbose_name=_('url'),)
    order       = models.IntegerField(default=0, verbose_name=_('order'),)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = _('Page Link')
        verbose_name_plural = _('Page Links')
        
    def delete(self):
        # delete translations
        Translation.objects.filter(
            table_name='PageLink',
            field_id=self.id
        ).delete()
        super(PageLink, self).delete()
        
    def trans_title(self):
        translation = get_translation('PageLink', 'title', self.id)
        if translation:
            return translation
        elif self.title:
            return self.title
        else:
            for lang, translation in get_translations('PageLink', 'title', self.id).items():
                if translation:
                    return translation
        return ''
        
    def all_trans_title(self):
        return get_translations('PageLink', 'title', self.id)

        
class PageHistory(TimeStampedModel):
    page        = models.ForeignKey("Page", on_delete=models.CASCADE)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, 
                                    on_delete=models.SET_NULL)
    data        = models.TextField()
    
        
# class PageAddress(TimeStampedModel):
#     page        = models.ForeignKey("Page", on_delete=models.CASCADE)
#     address     = models.TextField(max_length=500, null=True, blank=True, verbose_name=_('address'),)
#     order       = models.IntegerField(default=0, verbose_name=_('order'),)
#     
#     class Meta:
#         ordering = ['order', 'id']
#         verbose_name = _('Page Link')
#         verbose_name_plural = _('Page Links')
 
        

        

