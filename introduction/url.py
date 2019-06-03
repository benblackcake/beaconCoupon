from django.urls import path,include
from django.views.generic import TemplateView


app_name='introduction'
urlpatterns=[
    path('',TemplateView.as_view(template_name='index2.html'),name='index2')
]