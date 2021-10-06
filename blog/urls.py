from django.conf.urls import url
from blog import views

urlpatterns = [
    url("",views.index,name = 'index')
]