from rest_framework.test import APITestCase
from django.conf import settings
from unittest.mock import patch


class TestGeneral(APITestCase):
    def setUp(self):
        self.url = "/user_service/api/v1/auth/check_phone/"

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
        self.url = "/user_service/api/v1/auth/check_phone/" 
        self.data = {"phone_number": "09999999999"} 
        redis_key = f"auth-otp:{self.data['phone_number']}"
        settings.REDIS_CLIENT.delete(redis_key)

    def test_required_parameters(self, mock_allow_request):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["phone_number"], ['This field is required.'])
    
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
    
    def test_active_old_otp(self, mock_allow_request):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["phone_number"],
                         ['An OTP already exists. Please wait for it to expire before requesting a new one.'])
    
    def test_ok(self, mock_allow_request):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], 'The OTP code has been sent')
        
        # check redis
        redis_key = f"auth-otp:{self.data['phone_number']}"
        user_code = settings.REDIS_CLIENT.get(redis_key)
        self.assertIsNotNone(user_code)
        settings.REDIS_CLIENT.delete(redis_key)