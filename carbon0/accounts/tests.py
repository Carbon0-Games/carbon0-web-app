from django.test import TestCase, RequestFactory
from accounts.models import Profile
from accounts.views import UserCreate



# Create your tests here.
class ProfileTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_get_profile_form(self):
        get_request = self.request_factory.get('accounts:signup')
        response = UserCreate.as_view()(get_request)
        self.assertEqual(response.status_code, 200)


    # def test_profile_creation(self):
    #     form_data = {
    #         'email': "suntimes@email.com",
    #         'fist_name': "Sonny",
    #         'last_name': "Purdue",
    #         'username': 'Sunny',
    #         'password1': 'LearnCode',
    #         'password2': 'LearnCode'
    #     }

    #     post_request = self.request_factory.post('accounts:signup', form_data)
    #     response = UserCreate.as_view()(post_request)

    #     self.assertEqual(response.status_code, 302)