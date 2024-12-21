from rest_framework.test import APITestCase
from django.conf import settings
from unittest.mock import patch

from user.models import User 


class TestGeneral(APITestCase):
    def setUp(self):
        self.url = "/user_service/api/v1/auth/check_phone/verify/"

    @patch("auth.views.CustomAuthRateThrottle.allow_request", return_value=True)
    def test_invalid_methods(self, mock_allow_request):       
        # Method GET:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        response_data = response.json()
        self.assertEqual(response_data["detail"], 'Method "GET" not allowed.')

        # Method PUT:
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 405)
        response_data = response.json()
        self.assertEqual(response_data["detail"], 'Method "PUT" not allowed.')

        # Method PATCH:
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, 405)
        response_data = response.json()
        self.assertEqual(response_data["detail"], 'Method "PATCH" not allowed.')

        # Method DELETE:
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 405)
        response_data = response.json()
        self.assertEqual(response_data["detail"], 'Method "DELETE" not allowed.')

    def test_throttling(self):
        from auth.views import CustomAuthRateThrottle

        throttle_rate_str = CustomAuthRateThrottle.rate 
        throttle_rate_int = int(throttle_rate_str.split('/')[0])
        for i in range(throttle_rate_int):
            response = self.client.get(self.url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 429)


@patch("auth.views.CustomAuthRateThrottle.allow_request", return_value=True)
class TestCheckPhone(APITestCase): 
    def setUp(self):
        self.url = "/user_service/api/v1/auth/check_phone/verify/" 
        self.phone_number = "09999999999"
        self.redis_key = f"auth-otp:{self.phone_number}"
        settings.REDIS_CLIENT.delete(self.redis_key)
        settings.REDIS_CLIENT.setex(self.redis_key, settings.OTP_TTL, "123456")
        self.valid_data = {"phone_number": self.phone_number, "code":"123456"}

    def test_required_parameters(self, mock_allow_request):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["phone_number"], ['This field is required.'])
        self.assertEqual(response_data["code"], ['This field is required.'])
    
    def test_validate_phone_number(self, mock_allow_request):
        response = self.client.post(self.url, data={"phone_number": "099999"})
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["phone_number"],
                         ["Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."])
        response = self.client.post(self.url, data={"phone_number": "0999999999a"})
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["phone_number"],
                         ["Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."])
    
    def test_invalid_otp(self, mock_allow_request):
        response = self.client.post(self.url, data={"phone_number": self.phone_number, "code": "654321"})
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["code"], ['Invalid OTP code.'])

    def test_expire_otp(self, mock_allow_request):
        settings.REDIS_CLIENT.delete(self.redis_key)
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["non_field_errors"], ['Phone number not found or OTP code is expired'])
        
    def test_ok_new_user(self, mock_allow_request):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 201)
        u = User.objects.get(phone_number=self.valid_data["phone_number"])
        self.assertEqual(u.phone_number, self.valid_data["phone_number"])

        response_data = response.json()
        self.assertIn("access", response_data)
        self.assertIsNotNone(response_data["access"])
        self.assertIn("refresh", response_data)
        self.assertIsNotNone(response_data["refresh"])
        
    
    def test_ok_login_user(self, mock_allow_request):
        User.objects.create(phone_number=self.valid_data["phone_number"])
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn("access", response_data)
        self.assertIsNotNone(response_data["access"])
        self.assertIn("refresh", response_data)
        self.assertIsNotNone(response_data["refresh"])
