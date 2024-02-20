from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ChangePasswordApiView, ProfileUserViewSet, RegisterApiView

router = DefaultRouter()
router.register("", ProfileUserViewSet, basename="user")

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
    path(
        "change_password/<int:pk>/",
        ChangePasswordApiView.as_view(),
        name="change_password",
    ),
]

urlpatterns += router.urls
