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
from restapi.firebase import *
from restapi.apiKeyConnection import *
from ssh import connect_to_ssh

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        response = {}
        try:
            user = loginFB(email,password)
            response['message'] = 'Success'
            response['idToken'] = user['idToken']
            response['code'] = 'SUC'

        except Exception as e:
                exception_str = str(e)
                print(e)
                if exception_str.find('EMAIL_NOT_FOUND')!=-1:
                    response['message'] = 'No Email Found'
                    response['code'] = 'NO_EM'
                elif exception_str.find('INVALID_EMAIL')!=-1:
                    response['message'] = 'Invalid Email'
                    response['code'] = 'IN_EM'
                elif exception_str.find('INVALID_PASSWORD')!=-1:
                    response['message'] = 'Invalid Password'
                    response['code'] = 'IN_PASS'
                elif exception_str.find('USER_DISABLED')!=-1:
                    response['message'] = 'User is banned. Please contact admininstrator'
                    response['code'] = 'USER_DISABLED'
                else:
                    response['message'] = 'Some Other Error'
                    response['code'] = 'SOME'
        return JsonResponse(response)

    else:
        return Response('Invalid Request Method', status=status.HTTP_400_BAD_REQUEST)

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

@csrf_exempt
def uploadFile(request):
    if request.method == 'POST':
        response = {}
        files = request.FILES['file']
        return JsonResponse({"Filename" : filename + '.json',"Success": "True"},safe=False)
        try:
            idToken = request.META.get('HTTP_AUTHORIZATION','')
            if idToken=='':
                response['message'] = 'idToken is empty'
                response['code'] = 'ID_EMPTY'
            else:
                uid = checkifValidUser(idToken)
                if uid!=None:
                    filename = random_filename(filename=str(files))
                    path = default_storage.save('json_keys/' + filename + '.json', ContentFile(files.read()))
                    (message,code) = addFiletoFirebase(filename)
                    response['message'] = message
                    response['code'] = code
                else:
                    response['message'] = 'Invalid User'
                    response['code'] = 'INV_USER'
        except Exception as e:
            exception_str = str(e)
            if exception_str.startswith('Incorrect') or exception_str.startswith('Wrong'):
                response['message'] = 'Invalid idToken'
                response['code'] = 'INV_ID'
            elif exception_str.startswith('Token expired'):
                response['message'] = 'Token has expired'
                response['code'] = 'EXP_TOKEN'
            else:
                response['message'] = 'Some Other Error'
                response['code'] = 'SOME'
                print(e)
        return JsonResponse(response)
    else:
        return Response('Invalid Request Method', status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        files = request.FILES['file']
        print(files)
        '''filename = random_filename(filename=str(files))
        path = default_storage.save('screenshots/' + filename, ContentFile(files.read()))
        print(default_storage.exists(path))
        if default_storage.exists(path):
            return Response('screenshots/' + filename, status=status.HTTP_201_CREATED)
        else:
            return Response('Error Uploading File', status=status.HTTP_400_BAD_REQUEST)
        '''
        return JsonResponse({"Success": "True"},safe=False)

@csrf_exempt
def connectDO(request):
    if request.method == 'POST':
        response = {}
        api = request.POST['api']
        server_name = request.POST['server_name'].trim()
        try:
            idToken = request.META.get('HTTP_AUTHORIZATION','')
            if idToken=='':
                response['message'] = 'idToken is empty'
                response['code'] = 'ID_EMPTY'
            else:
                uid = checkifValidUser(idToken)
                if uid!=None:
                    (ip_address,message,code) = createServerDO(api,uid,server_name)
                    response['ip_address'] = ip_address
                    response['message'] = message
                    response['code'] = code
                else:
                    response['message'] = 'Invalid User'
                    response['code'] = 'INV_USER'
        except Exception as e:
            exception_str = str(e)
            if exception_str.startswith('Incorrect') or exception_str.startswith('Wrong'):
                response['message'] = 'Invalid idToken'
                response['code'] = 'INV_ID'
            elif exception_str.startswith('Token expired'):
                response['message'] = 'Token has expired'
                response['code'] = 'EXP_TOKEN'
            else:
                response['message'] = 'Some Other Error'
                response['code'] = 'SOME'
                print(e)
        return JsonResponse(response)
    else:
        return Response('Invalid Request Method', status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def connectAWS(request):
        host = request.POST['ipaddress']
        domain = request.POST['domain']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        uid = request.POST['uid']
        connect_to_ssh(host=host,domain=domain,username=username,password=password,email=email,uid=uid)
        return JsonResponse({"Success": "True"},safe=False)

@csrf_exempt
def connectGCP(request):
        host = request.POST['ipaddress']
        domain = request.POST['domain']
        username = request.POST['username']
        email = request.POST['email']
        uid = request.POST['uid']
        connect_to_ssh(host=host,domain=domain,username=username,password=password,email=email,uid=uid)
        return JsonResponse({"Success": "True"},safe=False)
