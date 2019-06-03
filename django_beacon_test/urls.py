
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path,include
from rest_framework.documentation import include_docs_urls

from beaconDashboard import dashboard_views
urlpatterns = [
    path('admin/',admin.site.urls),
    path('dashboard/',include('django.contrib.auth.urls')),
    path('dashboard/',include('beaconDashboard.url',namespace='beaconDashboard')),
    path('intro/',include('introduction.url',namespace='introduction')),
    path('docs/',include_docs_urls(title='My API title', public=False)),
    # path('hello/',include('beaconDashboard.url')),
    # path('home/',views.home ,name='home'),
    # path('hello/',views.hello,name='hello')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
print(urlpatterns)
#+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# path('(?P<hello>\w+)',views.hello)