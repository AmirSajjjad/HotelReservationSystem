from django.urls import path
from auth.views import AuthCheckPhoneAPIView, AuthVerifyCodeAPIView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('check_phone/', AuthCheckPhoneAPIView.as_view(), name="check_phone"),
    path('check_phone/verify/', AuthVerifyCodeAPIView.as_view()),  # Register or Login and give access token
    path('refresh_token', TokenRefreshView.as_view()),
]
