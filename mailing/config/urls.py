from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mailing/', include('mailing_service.urls')),
    path('users/', include('users.urls')),
    path('blog/', include('blog.urls')),
    path('home/', include('home.urls'))


]
