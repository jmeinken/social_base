import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import models
from main.helpers import constants



@csrf_exempt
def upload(request):
    if request.POST and 'image' in request.POST:
        image = request.POST.get('image')
        file_base_name = request.POST.get('base_name', None)
        imageArr = image.split(',')
        oImage = models.Image(file_base_name=file_base_name)
        oImage.save()
        file_name = oImage.get_image_name()
        print(file_name)
        fh = open(constants['UPLOADS_DIRECTORY'] + file_name, "wb")
        fh.write(imageArr[1].decode('base64'))
        fh.close()
    data = {
        'name' : file_name,
        'path' : constants['UPLOADS_URL_PATH'] + file_name
    }
    return HttpResponse(json.dumps(data), content_type = "application/json")

def get_path(request):
    if request.GET and 'image_name' in request.GET:
        file_name = request.GET.get('image_name')
        data = {
            'name' : file_name,
            'path' : constants['UPLOADS_URL_PATH'] + file_name
        }
    return HttpResponse(json.dumps(data), content_type = "application/json")