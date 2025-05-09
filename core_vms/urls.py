"""
URL configuration for core_vms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# src/urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
# from vmsapp.views.appointment.read import audio_call,audio_call2

admin.site.site_header = "Visitor Management Admin"
admin.site.site_title = "VMS Admin"
admin.site.index_title = "Welcome to VMS Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('authuser.urls')),
    path('api/', include('vmsapp.urls')),
    # path('realtime', include('demo.urls')),
    # path('api/', include('webshocket.urls')),
    path('', include('frontent.urls',namespace="frontent")),
    # path('audio_call/', audio_call, name='audio_call'),
    # path('audio_call2/', audio_call2, name='audio_call2'),

]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)