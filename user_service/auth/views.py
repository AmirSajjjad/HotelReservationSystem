from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema

from auth.serializers import (
    CheckPhoneNumberRequestSerializer,
    CheckPhoneNumberResponseSerializer,
    ValidateCodeRequestSerializer ,
    TokenResponseSerializer
)
from auth.tasks import send_sms_otp
from user_service.utils import generate_otp, get_tokens_for_user
from user.models import User


class CustomAuthRateThrottle(AnonRateThrottle): 
    rate = '3/minute'


class AuthCheckPhoneAPIView(APIView):
    throttle_classes = [CustomAuthRateThrottle]

    @swagger_auto_schema(
        query_serializer=CheckPhoneNumberRequestSerializer, 
        responses={
            200: CheckPhoneNumberResponseSerializer
        } 
    )
    def post(self, request,*args, **kwargs):
        serializer = CheckPhoneNumberRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        redis_key = f"auth-otp:{phone_number}"

        if settings.REDIS_CLIENT.exists(redis_key):
            return Response(
                {'phone_number': ['An OTP already exists. Please wait for it to expire before requesting a new one.']},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_code = generate_otp(settings.OTP_DIGITS_NUMBER)
        settings.REDIS_CLIENT.setex(redis_key, settings.OTP_TTL, otp_code)
        send_sms_otp.delay(phone_number, otp_code)
    
        response = {"message": "The OTP code has been sent"}
        if settings.DEBUG:
            response["code"] = otp_code

        response_serializer = CheckPhoneNumberResponseSerializer(response)
        return Response(response_serializer.data)


class AuthVerifyCodeAPIView(APIView):
    throttle_classes = [CustomAuthRateThrottle]

    @swagger_auto_schema(
        query_serializer=ValidateCodeRequestSerializer, 
        responses={
            200: TokenResponseSerializer
        } 
    )
    def post(self, request,*args, **kwargs):
        serializer = ValidateCodeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data["phone_number"]
        otp_code = serializer.validated_data["code"]

        redis_key = f"auth-otp:{phone_number}"
        
        user_code = settings.REDIS_CLIENT.get(redis_key)
        if not user_code:
            return Response({'non_field_errors': ['Phone number not found or OTP code is expired']},
                            status=status.HTTP_400_BAD_REQUEST)
        if not user_code.decode() == otp_code:
            return Response({'code': ['Invalid OTP code.']},
                            status=status.HTTP_400_BAD_REQUEST)
        settings.REDIS_CLIENT.delete(redis_key)

        user, created = User.objects.get_or_create(phone_number=phone_number)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        response = TokenResponseSerializer(get_tokens_for_user(user))
        return Response(response.data, status=status_code)
