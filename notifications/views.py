import json

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import HttpResponse

from . import models



def ajax_alerts(request):
    context = {}
    user_id = request.GET.get(user_id, 0)
    oUser = get_user_model().objects.all().get(pk=user_id)
    qAlert = models.NotificationRecipient.objects.filter(recipient=oUser).filter(alert_queue=True)
    context['qAlert'] = qAlert
    html = render_to_string('notifications/alerts.html', context)
    data = {}
    data['html'] = html
    data['count'] = qAlert.count()
    return HttpResponse(json.dumps(data), content_type = "application/json")
        
