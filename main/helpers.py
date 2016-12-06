# -*- coding: utf-8 -*-


# This is added as a context processor in settings_global.TEMPLATES
# it is already available in your templates
# To use other places in your code, access it directly here

constants = {}
constants['TITLE'] = 'Social Base'
constants['LOGO'] = '<i class="fa fa-user-circle-o fa-lg" aria-hidden="true"></i>'
constants['CONTACT_EMAIL'] = 'info@cincinnati-jouhou.com'
constants['UPLOADS_DIRECTORY'] = '/home/ubuntu/django/social-base-env/social_base/static/uploads/'
constants['UPLOADS_URL_PATH'] = '/static/uploads/'
constants['LOGS_DIRECTORY'] = '/home/ubuntu/django/social-base-env/social_base/logs/'
constants['BASE_URL'] = 'http://johnmeinken.com'


def get_constants(request=None):
    return {'constants' : constants}