from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.views import ListCreateUser, RetrieveUpdateDestroyUser, MyTokenObtainPairView

User = get_user_model()


class TestUrls(TestCase):
    """Test that views have the correct routing"""

    def test_list_create_users_url_resolve(self):
        url = reverse('list_create_users')
        self.assertEquals(resolve(url).func.view_class, ListCreateUser)

    def test_retrieve_update_destroy_user_url_resolve(self):
        self.test_user = User.objects.create(id=1,
                                             email='robert@gmail.com',
                                             first_name='Robert',
                                             last_name='López Pérez',
                                             role='D',
                                             mobile_phone='+34 10101023',
                                             password='PasswordStrong1234')
        url = reverse('retrieve_update_destroy_user', args=[1])
        self.assertEquals(resolve(url).func.view_class, RetrieveUpdateDestroyUser)

    def test_token_obtain_pair_url_resolve(self):
        url = reverse('token_obtain_pair')
        self.assertEquals(resolve(url).func.view_class, MyTokenObtainPairView)
