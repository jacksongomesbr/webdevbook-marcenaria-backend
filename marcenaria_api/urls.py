from django.conf.urls import url, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'grupos', GroupViewSet)
router.register(r'materiais', MaterialViewSet)
router.register(r'placas', PlacaViewSet)
router.register(r'recortes-retangulares', RecorteRetangularViewSet)
router.register(r'recortes-triangulares', RecorteTriangularViewSet)
router.register(r'recortes-circulares', RecorteCircularViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', checklogin_view, name='checklogin'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
