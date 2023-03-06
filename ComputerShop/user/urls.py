from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = "user"

urlpatterns = [
      path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      path('register/',views.RegistrationAPI.as_view(),name="registration"),
      path('getUserInfor/',views.getUserInforAPI.as_view(),name="getuserinfor"),
      path('refreshPassword/',views.refreshPasswordAPI.as_view(),name="refreshPassword"),
      path('updateUserInfor/',views.updateUserInforAPI.as_view(),name="updateuserinfor"),
      path('updateEmail/',views.updateEmailAPI.as_view(),name="updateemail"),
]