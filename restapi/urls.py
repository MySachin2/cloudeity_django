from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^imageUpload$', views.FileUploadView.as_view()),
    url(r'^login$', views.login,name='login'),
    url(r'^launchServer$', views.sshFreeServer,name='launchServer'),
    url(r'^uploadFile$', views.FileUploadView.as_view()),
    url(r'^connect/do$', views.connectDO,name='connectDO'),
    url(r'^connect/gcp$', views.connectGCP,name='connectGCP'),
    url(r'^connect/aws$', views.connectAWS,name='connectAWS')
]
