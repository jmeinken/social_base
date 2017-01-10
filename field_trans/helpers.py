
from django.utils import translation

from . import models

def get_verbose_language(code):
    if code == 'ja':
        return 'Japanese'
    if code == 'en':
        return 'English'
    return ''

def set_translation(table_name, field_name, field_id, language_id, text):
    qTranslation = models.Translation.objects.filter(table_name=table_name).filter(field_name=field_name).filter(field_id=field_id).filter(language_id=language_id)
    if qTranslation:
        oTranslation = qTranslation[0]
        oTranslation.text = text
        oTranslation.save()
    else:
        if text:
            oTranslation = models.Translation(table_name=table_name,field_name=field_name,field_id=field_id,language_id=language_id,text=text)
            oTranslation.save()
    
def get_translation(table_name, field_name, field_id):
    language = translation.get_language()
    qTranslation = models.Translation.objects.filter(table_name=table_name).filter(field_name=field_name).filter(field_id=field_id).filter(language=language)
    if qTranslation:
        text = qTranslation[0].text
        if text == '':
            return False
        else:
            return text
    else:
        return False
    
def get_translations(table_name, field_name, field_id):
    qTranslation = models.Translation.objects.filter(table_name=table_name).filter(field_name=field_name).filter(field_id=field_id)
    result = {}
    for oTranslation in qTranslation:
        result[oTranslation.language.code] = oTranslation.text
    return result
        