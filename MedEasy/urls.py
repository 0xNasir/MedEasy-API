"""
URL configuration for MedEasy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

schema_view = get_schema_view(
    openapi.Info(
        title="MedEasy API",
        default_version='v 1.0',
        description="MedEasy description"
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='docs/')),
    path('auth/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('v1/api/', include('medicine.urls', namespace='product')),
    path('accounts/', include('rest_framework.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
