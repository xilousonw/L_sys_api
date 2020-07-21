from django.urls import path,re_path,include
from . import views
from rest_framework.routers import SimpleRouter

router=SimpleRouter()
router.register('banner',views.BannerViewSet,'banner')
urlpatterns = [
    path('',include(router.urls)),
]