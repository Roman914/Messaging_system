from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls', app_name), namespace="messages-api")),
    path('api-token-auth/', obtain_auth_token),

]
