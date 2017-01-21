
import datetime

from django.core.mail import send_mail

from main.helpers import constants






def send_system_mail(
            subject,                # string
            message,                # plain text version
            html_message,            # html version
            from_mail,               # sender email address
            to_list,                 # list of recipient emails
            fail_silently=False
    ):
    subject = '[' + constants['TITLE'] + '] ' + subject
    try:
        send_mail(subject, message, from_mail, to_list, fail_silently, html_message=html_message)
        action = 'SENT'
    except:
        action = 'FAIL'
    logDir = constants['LOGS_DIRECTORY']
    myFile = open(logDir + 'emails.txt', 'a+')
    myFile.write(
        action + '\t' +
        str(datetime.datetime.now()) + '\t' +
        subject.encode('utf8') + '\t' +
        'from:' + from_mail + '\t' +
        'to:' + str(to_list) + '\n'
    )
    myFile.close()
    myFile = open(logDir + 'emails_full.txt', 'a+')
    myFile.write(
        '-----------------------------------------------------' + '\n'
        'time: ' + str(datetime.datetime.now()) + '\n' +
        'subject: ' + subject.encode('utf8') + '\n' +
        'from: ' + from_mail + '\n' +
        'to: ' + str(to_list) + '\n' + 
        'body:' + '\n' + 
        message.encode('utf8') + '\n' + 
        '-----------------------------------------------------' + '\n'
    )
    myFile.close()
    if action == 'SENT':
        return True
    else:
        return False
    
    
    
    