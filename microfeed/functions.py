import re


def replace_url_to_link(value):
    # Replace url to link
    urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="\1" target="_blank">\1</a>', value)
    # Replace email to mailto
    urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="mailto:\1">\1</a>', value)
    return value

def process_post_body(value):
    value = value.replace('\n', '<br />')
    value = value.replace(' www.', ' http://www.')
    value = replace_url_to_link(value)
    return value

def process_comment_body(value):
    value = value.replace('\n', '<br />')
    value = value.replace(' www.', ' http://www.')
    value = replace_url_to_link(value)
    return value

