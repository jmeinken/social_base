# -*- coding: utf-8 -*-


# This is added as a context processor in settings_global.TEMPLATES
# it is already available in your templates
# To use other places in your code, access it directly here

constants = {}
constants['TITLE'] = 'Social Base'
constants['LOGO'] = '<i class="fa fa-user-circle-o fa-lg" aria-hidden="true"></i>'
constants['CONTACT_EMAIL'] = 'thebellsofohio@hotmail.com'
constants['UPLOADS_DIRECTORY'] = '/home/ubuntu/django/social-base-env/social_base/static/uploads/'
constants['UPLOADS_URL_PATH'] = '/static/uploads/'

def get_constants(request=None):
    return {'constants' : constants}