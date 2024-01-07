from rest_framework.routers import DefaultRouter

from medicine.views import ProductAPIView

"""
app_name is added as the app has a namespace.
"""
app_name = 'medicine'

"""
initiate the default router.
next url will be registered to the router.
"""
router = DefaultRouter()
router.register('product', ProductAPIView, basename='product')
urlpatterns = router.urls
