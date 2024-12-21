from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="Your Project API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('user_service/admin/', admin.site.urls),
    path('user_service/api/v1/auth/', include('auth.urls')),
    path('user_service/api/v1/user/', include('user.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('user_service/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('user_service/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
