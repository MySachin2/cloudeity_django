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

def index(request):
    json_output = []
    categories = Category.objects.all()
    for c in categories:
        json_output.append({'category_name' : c.category_name, 'image_url' : c.image_url})
    return JsonResponse(json_output,safe=False)

@csrf_exempt
def uploadFeedback(request):
    screenshot = request.POST.get('filename','')
    name = request.POST.get('name','')
    feedback_type = request.POST.get('feedback_type','')
    description = request.POST.get('description','')
    print("Type" + feedback_type)
    print("name" + name)
    print("description" + description)
    if description=='' or name=='' or feedback_type=='':
        return JsonResponse({"Success": "False"},safe=False)
    f = Feedback(name=name,type_of_feedback=feedback_type,description=description,screenshot=screenshot)
    f.save()
    return JsonResponse({"Success": "True"},safe=False)

def get_csrf_token(request):
    token = csrf.get_token(request)
    return JsonResponse({'token': token},safe=False)

@csrf_exempt
def deleteFile(request):
    filename = request.POST.get('filename','')
    if filename:
        if default_storage.exists(filename):
            default_storage.delete(filename)
            return JsonResponse({"Success": "True"},safe=False)
    return JsonResponse({"Success": "False"},safe=False)


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
