from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

'''path urls to different applications'''
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path("LITreview/", include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
