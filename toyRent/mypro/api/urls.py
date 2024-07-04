from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'yourmodel', views.YourModelViewSet)


urlpatterns = [
    path("view/",views.view,name="view"),
    path("update/",views.update,name="update"),
    path("subcategory/",views.subcategories,name="subcategory"),




    path("",include(router.urls)),
]
