from django.http import JsonResponse
from .models import Category,Feedback
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from .functions import pretty_request
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .functions import random_filename

from ssh import connect_to_ssh

@csrf_exempt
def deleteFile(request):
    filename = request.POST.get('filename','')
    if filename:
        if default_storage.exists(filename):
            default_storage.delete(filename)
            return JsonResponse({"Success": "True"},safe=False)
    return JsonResponse({"Success": "False"},safe=False)

@csrf_exempt
def sshFreeServer(request):
        host = request.POST['ipaddress']
        domain = request.POST['domain']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        uid = request.POST['uid']
        connect_to_ssh(host=host,domain=domain,username=username,password=password,email=email,uid=uid)
        return JsonResponse({"Success": "True"},safe=False)

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        files = request.FILES['screenshot']
        filename = random_filename(filename=str(files))
        path = default_storage.save('screenshots/' + filename, ContentFile(files.read()))
        print(default_storage.exists(path))
        if default_storage.exists(path):
            return Response('screenshots/' + filename, status=status.HTTP_201_CREATED)
        else:
            return Response('Error Uploading File', status=status.HTTP_400_BAD_REQUEST)
