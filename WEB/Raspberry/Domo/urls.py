from rest_framework import routers

from Domo.views import SensorViewSet, MotorViewSet

router = routers.DefaultRouter()
router.register(r'sensors', SensorViewSet)
router.register(r'motors', MotorViewSet)

urlpatterns = router.urls
