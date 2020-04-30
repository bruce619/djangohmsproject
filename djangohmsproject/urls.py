from django.contrib import admin
from django.urls import path, include
from healthapp.views import home
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('healthapp.urls')),
]
#  Saves static files in static folder
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = home.error_404
handler500 = home.error_500
