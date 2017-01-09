import re

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


def replace_url_to_link(value):
    # Replace url to link
    urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="\1" target="_blank">\1</a>', value)
    # Replace email to mailto
    urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="mailto:\1">\1</a>', value)
    return value

def pretty_html(value):
    value = value.replace('\n', '<br />')
    value = value.replace(' www.', ' http://www.')
    value = replace_url_to_link(value)
    return value




