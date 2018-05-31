from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^imageUpload$', views.FileUploadView.as_view()),
    url(r'^connect$', views.sshFreeServer,name='connect')
]
