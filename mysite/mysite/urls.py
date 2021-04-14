import os
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.views.static import serve

# Up two folders to serve "site" content
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.join(BASE_DIR, 'site')

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('webnavigate/', include('webnavigate.urls')),
]