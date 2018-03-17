from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^categories$', views.index, name='index'),
    url(r'^imageUpload$', views.FileUploadView.as_view()),
    url(r'^get-token$', views.get_csrf_token),
    url(r'^uploadFeedback$', views.uploadFeedback,name='uploadFeedback'),
    url(r'^deleteFile$', views.deleteFile,name='deleteFile'),
    url(r'^testFirebase$', views.testFirebase,name='testFirebase'),
]
