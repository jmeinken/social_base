
from . import models



def create_notification(
            qRecipient,             # queryset or simple array of User model objects
            oCategory,              # (Notification) Category model object
            html_short,
            html_long,
            plain_text_short,
            plain_text_long,
            image = None,           # full html path to image
            link = None             # full html path to link   
    ):
    oNotification = models.Notification(
        category = oCategory,
        html_short = html_short,
        html_long = html_long,
        plain_text_short = plain_text_short,
        plain_text_long = plain_text_long,
        image = image,
        link = link                            
    )
    oNotification.save()
    for oRecipient in qRecipients:
        oNR = models.NotificationRecipient(
            recipient = oRecipient,
            notification = oNotification,                              
        )
        oNR.save()  
    return oNotification.id

def update_notification_data(
            notification_id,             # queryset or simple array of User model objects
            oCategory,              # (Notification) Category model object
            html_short,
            html_long,
            plain_text_short,
            plain_text_long,
            image = None,           # full html path to image
            link = None             # full html path to link   
    ):
    oNotification = models.Notification.objects.all().get(pk=notification_id)
    oNotification.category = oCategory
    oNotification.html_short = html_short
    oNotification.html_long = html_long
    oNotification.plain_text_short = plain_text_short
    oNotification.plain_text_long = plain_text_long
    oNotification.image = image
    oNotification.link = link
    oNotification.save()
    return oNotification.id

def update_notification_recipients(notification_id, qRecipient):
    pass

def update_notification(
            notification_id,             # queryset or simple array of User model objects
            qRecipient,
            oCategory,              # (Notification) Category model object
            html_short,
            html_long,
            plain_text_short,
            plain_text_long,
            image = None,           # full html path to image
            link = None             # full html path to link   
    ):
    pass

def delete_notification(notification_id):
    oNotification = models.Notification.objects.all().get(pk=notification_id)
    oNotification.delete()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    