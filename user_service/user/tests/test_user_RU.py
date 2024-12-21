from rest_framework.test import APITestCase
from user.models import User


class TestGeneral(APITestCase):
    def setUp(self) -> None:
        self.phone_number = "+999999999"
        self.url = "/user_service/api/v1/user/"
        self.user = User.objects.create(phone_number=self.phone_number)

    def test_invalid_methods(self):
        self.client.force_authenticate(user=self.user)
        
        # Method POST:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        response_data = response.json()
        self.assertEqual(response_data["detail"], 'Method "POST" not allowed.')

        # Method DELETE:
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 405)
        response_data = response.json()
        self.assertEqual(response_data["detail"], 'Method "DELETE" not allowed.')


class TestRetriveUser(APITestCase):

    def setUp(self) -> None:
        self.phone_number = "+999999999"
        self.url = "/user_service/api/v1/user/"
        self.user = User.objects.create(phone_number=self.phone_number)

    def test_not_autenticate(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        response_data = response.json()
        self.assertEqual(response_data["detail"], 'Authentication credentials were not provided.')
    
    def test_ok(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["phone_number"], self.user.phone_number)
        self.assertEqual(response_data["first_name"], self.user.first_name)
        self.assertEqual(response_data["last_name"], self.user.last_name)
        self.assertEqual(response_data["national_id"], self.user.national_id)


class TestUpdateUser(APITestCase):
    def setUp(self):
        self.phone_number = "+999999999"
        self.url = "/user_service/api/v1/user/"
        self.user = User.objects.create(phone_number=self.phone_number)
        self.data = {
            "password" : "123",
            "first_name": "first_name",
            "last_name": "last_name",
            "national_id": "1234567890",
        }

    def test_not_autenticate(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        response_data = response.json()
        self.assertEqual(response_data["detail"], 'Authentication credentials were not provided.')
    
    def test_validations(self):
        self.client.force_authenticate(user=self.user)
        # coud not change phone number
        response = self.client.patch(self.url, data={"phone_number": "09111111111"})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["phone_number"], self.user.phone_number)

        # test national_id not only digit
        response = self.client.patch(self.url, data={"national_id": "123456789a"})
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["national_id"], ['national_id must be only digit'])

        # test len national_id
        response = self.client.patch(self.url, data={"national_id": "123456789"})
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["national_id"], ["national_id is 10 digit"])

        # test required data
        response = self.client.put(self.url, data={})
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["first_name"], ['This field is required.'])
        self.assertEqual(response_data["last_name"], ['This field is required.'])
        self.assertEqual(response_data["national_id"], ['This field is required.'])

    def test_ok(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["phone_number"], self.user.phone_number)
        self.assertEqual(response_data["first_name"], self.data["first_name"])
        self.assertEqual(response_data["last_name"], self.data["last_name"])
        self.assertEqual(response_data["national_id"], self.data["national_id"])
