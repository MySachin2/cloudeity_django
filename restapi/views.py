from django.http import JsonResponse
from .models import Category
def index(request):
    json_output = []
    categories = Category.objects.all()
    for c in categories:
        json_output.append({'Category' : c.category_name})
    print json_output
    return JsonResponse(json_output,safe=False)
