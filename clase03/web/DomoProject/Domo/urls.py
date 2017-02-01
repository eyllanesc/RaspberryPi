from rest_framework import routers

from Domo.views import SensorViewSet

router = routers.DefaultRouter()
router.register(r'sensors', SensorViewSet)

urlpatterns = router.urls
