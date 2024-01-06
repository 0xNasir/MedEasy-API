from rest_framework.routers import DefaultRouter

from medicine.views import ProductAPIView

app_name = 'medicine'
router = DefaultRouter()
router.register('product', ProductAPIView, basename='product')
urlpatterns = router.urls
