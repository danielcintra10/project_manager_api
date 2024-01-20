from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TestListCreateUser(APITestCase):
    """Test /api/v1/accounts/users/ endpoint, check responses, permissions and constraints"""

    def setUp(self):
        self.test_pm_user = User.objects.create_user(email='robert@gmail.com',
                                                     first_name='Robert',
                                                     last_name='Lopez',
                                                     role='P',
                                                     mobile_phone='+53 59876543',
                                                     password='Pass*2024*')

        self.test_dev_user = User.objects.create_user(email='jeni@gmail.com',
                                                      first_name='Jeni',
                                                      last_name='Anderson',
                                                      role='D',
                                                      mobile_phone='+1 897456210',
                                                      password='2024-the-year')

        self.test_super_user = User.objects.create_superuser(email='dany@gmail.com',
                                                             first_name='Daniel',
                                                             last_name='Perez',
                                                             role='P',
                                                             mobile_phone='+53 54876543',
                                                             password='Hummer45#')
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_super_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/accounts/users/')
        self.assertEqual(response.status_code, 401)

    def test_get_request_access_authenticated_dev_user_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/')
        self.assertEqual(response.status_code, 403)

    def test_get_request_admin_user_returns_200(self):
        response = self.client.get('/api/v1/accounts/users/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_pm_user_returns_200(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/')
        self.assertEqual(response.status_code, 200)

    def test_post_request_create_user_with_valid_data_returns_201(self):
        data = {
            'email': 'camille@gmail.com',
            'first_name': 'Camila',
            'last_name': 'Ernst',
            'role': 'Developer',
            'mobile_phone': '+53 89410023',
            'password': 'CamiOop44',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 201)

    def test_post_request_create_correct_new_user_db_count_equal_4(self):
        data = {
            'email': 'camille@gmail.com',
            'first_name': 'Camila',
            'last_name': 'Ernst',
            'role': 'Developer',
            'mobile_phone': '+53 89410023',
            'password': 'CamiOop44',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 4)

    def test_post_request_return_correct_data(self):
        data = {
            'email': 'camille@gmail.com',
            'first_name': 'Camila',
            'last_name': 'Ernst',
            'role': 'Developer',
            'mobile_phone': '+53 89410023',
            'password': 'CamiOop44',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 4)
        user = User.objects.filter(email__exact="camille@gmail.com").first()
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["mobile_phone"], user.mobile_phone)
        self.assertEqual(response.data["role"], user.get_role_display())
        self.assertEqual(response.data["is_active"], user.is_active)

    def test_post_request_new_user_password_is_encrypted_ok(self):
        data = {
            'email': 'camille@gmail.com',
            'first_name': 'Camila',
            'last_name': 'Ernst',
            'role': 'Developer',
            'mobile_phone': '+53 89410023',
            'password': 'CamiOop44',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        user = User.objects.filter(email__exact='camille@gmail.com').first()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(user.check_password('CamiOop44'))

    def test_post_request_validate_email_unique_constraint(self):
        data = {
            'email': 'dany@gmail.com',
            'first_name': 'Camila',
            'last_name': 'Ernst',
            'role': 'Developer',
            'mobile_phone': '+53 89410023',
            'password': 'CamiOop44',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_validate_mobile_phone_unique_constraint(self):
        data = {
            'email': 'camille@gmail.com',
            'first_name': 'Camila',
            'last_name': 'Ernst',
            'role': 'Developer',
            'mobile_phone': '+53 59876543',
            'password': 'CamiOop44',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_validate_secure_password(self):
        data = {
            'email': 'camille@gmail.com',
            'first_name': 'Camila',
            'last_name': 'Ernst',
            'role': 'Developer',
            'mobile_phone': '+53 89410023',
            'password': '1234',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_wrong_email(self):
        data = {
            'email': 'email',
            'first_name': 'Camila',
            'last_name': 'Ernst',
            'role': 'Developer',
            'mobile_phone': '+53 89410023',
            'password': 'CamiOop44',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_wrong_first_name(self):
        data = {
            'email': 'camille@gmail.com',
            'first_name': 'Camila87**',
            'last_name': 'Ernst',
            'role': 'Developer',
            'mobile_phone': '+53 89410023',
            'password': 'CamiOop44',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_wrong_last_name(self):
        data = {
            'email': 'camille@gmail.com',
            'first_name': 'Camila',
            'last_name': 'Ernst88**',
            'role': 'Developer',
            'mobile_phone': '+53 89410023',
            'password': 'CamiOop44',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_wrong_mobile_phone(self):
        data = {
            'email': 'camille@gmail.com',
            'first_name': 'Camila',
            'last_name': 'Ernst',
            'role': 'Developer',
            'mobile_phone': '+53 ahy98*/',
            'password': 'CamiOop44',
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)


class TestRetrieveUpdateDestroyUser(APITestCase):
    """Test /api/v1/accounts/users/{id_user} endpoint, check responses and permissions"""

    def setUp(self):
        self.test_pm_user = User.objects.create_user(id=1,
                                                     email='robert@gmail.com',
                                                     first_name='Robert',
                                                     last_name='Lopez',
                                                     role='P',
                                                     mobile_phone='+53 59876543',
                                                     password='Pass*2024*')

        self.test_dev_user = User.objects.create_user(id=2,
                                                      email='jeni@gmail.com',
                                                      first_name='Jeni',
                                                      last_name='Anderson',
                                                      role='D',
                                                      mobile_phone='+1 897456210',
                                                      password='2024-the-year')

        self.test_super_user = User.objects.create_superuser(id=3,
                                                             email='dany@gmail.com',
                                                             first_name='Daniel',
                                                             last_name='Perez',
                                                             role='P',
                                                             mobile_phone='+53 54876543',
                                                             password='Hummer45#')
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_super_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 401)

    def test_get_request_access_authenticated_admin_user_returns_200(self):
        response = self.client.get('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 200)

    def test_get_request_access_authenticated_pm_user_returns_200(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 200)

    def test_get_request_access_authenticated_dev_user_owner_returns_200(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/2')
        self.assertEqual(response.status_code, 200)

    def test_get_request_access_authenticated_dev_user_no_owner_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 403)

    def test_get_request_return_correct_data_admin_user_authenticated(self):
        response = self.client.get('/api/v1/accounts/users/1')
        user = User.objects.filter(email__exact="robert@gmail.com").first()
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["mobile_phone"], user.mobile_phone)
        self.assertEqual(response.data["role"], user.get_role_display())
        self.assertEqual(response.data["is_active"], user.is_active)

    def test_get_request_return_correct_data_pm_user_authenticated(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/1')
        user = User.objects.filter(email__exact="robert@gmail.com").first()
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["mobile_phone"], user.mobile_phone)
        self.assertEqual(response.data["role"], user.get_role_display())
        self.assertEqual(response.data["is_active"], user.is_active)

    def test_get_request_return_correct_data_dev_user_authenticated_and_owner(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/2')
        user = User.objects.filter(email__exact="jeni@gmail.com").first()
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["mobile_phone"], user.mobile_phone)
        self.assertEqual(response.data["role"], user.get_role_display())
        self.assertEqual(response.data["is_active"], user.is_active)

    def test_get_request_access_authenticated_pm_user_cant_see_super_users_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/3')
        self.assertEqual(response.status_code, 404)

    def test_put_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        # first_name, mobile_phone fields are updated
        data = {
            'email': 'robert@gmail.com',
            'first_name': 'Robertico JR',
            'last_name': 'Lopez',
            'role': 'Project Manager',
            'mobile_phone': '+53 598765000',
            'password': 'Pass*2024*',
        }
        response = self.client.put('/api/v1/accounts/users/1', data=data)
        self.assertEqual(response.status_code, 401)

    def test_put_request_access_authenticated_pm_user_no_owner_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'email': 'boby@gmail.com',
            'first_name': 'Robertico JR',
            'last_name': 'Lopez',
            'role': 'Project Manager',
            'mobile_phone': '+59 598787000',
            'password': 'Pass*2024*',
        }
        response = self.client.put('/api/v1/accounts/users/2', data=data)
        self.assertEqual(response.status_code, 403)

    def test_put_request_access_authenticated_dev_user_no_owner_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'email': 'robert@gmail.com',
            'first_name': 'Robertico JR',
            'last_name': 'Lopez',
            'role': 'Project Manager',
            'mobile_phone': '+53 598765000',
            'password': 'Pass*2024*',
        }
        response = self.client.put('/api/v1/accounts/users/1', data=data)
        self.assertEqual(response.status_code, 403)

    def test_put_request_admin_user_authenticated_returns_200(self):
        data = {
            'email': 'robert@gmail.com',
            'first_name': 'Robertico JR',
            'last_name': 'Lopez',
            'role': 'Project Manager',
            'mobile_phone': '+53 598765070',
            'password': 'Pass*2024*',
        }
        response = self.client.put('/api/v1/accounts/users/1', data=data)
        self.assertEqual(response.status_code, 200)

    def test_put_request_pm_user_authenticated_and_owner_returns_200(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'email': 'robert@gmail.com',
            'first_name': 'Robertico JR',
            'last_name': 'Lopez',
            'role': 'Project Manager',
            'mobile_phone': '+53 598765070',
            'password': 'Pass*2024*',
        }
        response = self.client.put('/api/v1/accounts/users/1', data=data)
        self.assertEqual(response.status_code, 200)

    def test_put_request_dev_user_authenticated_and_owner_returns_200(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'email': 'jeni@gmail.com',
            'first_name': 'Jennifer',
            'last_name': 'Torres',
            'role': 'Project Manager',
            'mobile_phone': '+34 85025455',
            'password': 'Pass*2024*',
        }
        response = self.client.put('/api/v1/accounts/users/2', data=data)
        self.assertEqual(response.status_code, 200)

    def test_put_request_admin_user_authenticated_returns_correct_data(self):
        data = {
            'email': 'bobby@gmail.com',
            'first_name': 'Bobby JR',
            'last_name': 'Know',
            'role': 'Developer',
            'mobile_phone': '+53 598767888',
            'password': 'Pass*new*pass*2024',
        }
        response = self.client.put('/api/v1/accounts/users/1', data=data)
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(email__exact="bobby@gmail.com").first()
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["mobile_phone"], user.mobile_phone)
        self.assertEqual(response.data["role"], user.get_role_display())
        self.assertEqual(response.data["is_active"], user.is_active)
        self.assertTrue(user.check_password('Pass*new*pass*2024'))

    def test_put_request_no_admin_user_authenticated_and_owner_returns_correct_data(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'email': 'bobby@gmail.com',
            'first_name': 'Bobby JR',
            'last_name': 'Know',
            'role': 'Developer',
            'mobile_phone': '+53 598767888',
            'password': 'Pass*new*pass*2024',
        }
        response = self.client.put('/api/v1/accounts/users/2', data=data)
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(email__exact="bobby@gmail.com").first()
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["mobile_phone"], user.mobile_phone)
        self.assertEqual(response.data["role"], user.get_role_display())
        self.assertEqual(response.data["is_active"], user.is_active)
        self.assertTrue(user.check_password('Pass*new*pass*2024'))

    def test_patch_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.patch('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 401)

    def test_patch_request_access_authenticated_pm_user_no_owner_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'email': 'boby@gmail.com',
            'first_name': 'Robertico JR',
            'last_name': 'Lopez',
            'role': 'Project Manager',
            'mobile_phone': '+59 598787000',
            'password': 'Pass*2024*',
        }
        response = self.client.patch('/api/v1/accounts/users/2', data=data)
        self.assertEqual(response.status_code, 403)

    def test_patch_request_access_authenticated_dev_user_no_owner_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        data = {
            'email': 'robert@gmail.com',
            'first_name': 'Robertico JR',
            'last_name': 'Lopez',
            'role': 'Project Manager',
            'mobile_phone': '+53 598765000',
            'password': 'Pass*2024*',
        }
        response = self.client.patch('/api/v1/accounts/users/1', data=data)
        self.assertEqual(response.status_code, 403)

    def test_user_can_update_password(self):
        data = {
            'password': 'Megan*742bin',
        }
        response = self.client.patch('/api/v1/accounts/users/1', data=data)
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(email__exact="robert@gmail.com").first()
        self.assertTrue(user.check_password('Megan*742bin'))

    def test_delete_no_authenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.delete('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 401)

    def test_delete_request_access_authenticated_pm_user_no_owner_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.delete('/api/v1/accounts/users/2')
        self.assertEqual(response.status_code, 403)

    def test_delete_request_access_authenticated_dev_user_no_owner_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.delete('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 403)

    def test_delete_request_access_authenticated_admin_user_returns_204(self):
        response = self.client.delete('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 204)

    def test_delete_request_access_authenticated_dev_user_owner_returns_204(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.delete('/api/v1/accounts/users/2')
        self.assertEqual(response.status_code, 204)

    def test_delete_request_access_authenticated_pm_user_owner_returns_204(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.delete('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 204)

    def test_delete_request_access_authenticated_admin_user_only_change_attributes_deleted_and_is_active(self):
        response = self.client.delete('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 204)
        user = User.objects.filter(email__exact="robert@gmail.com").first()
        self.assertFalse(user.is_active)
        self.assertTrue(user.deleted)


class TestLoginUser(APITestCase):
    """Test /api/v1/accounts/users/login endpoint, check responses and correct login credentials"""

    def setUp(self):
        self.test_user = User.objects.create_user(id=1,
                                                  email='robert@gmail.com',
                                                  first_name='Robert',
                                                  last_name='Lopez',
                                                  role='P',
                                                  mobile_phone='+53 59876543',
                                                  password='Pass*2024*')
        self.client = APIClient()

    def test_post_request_with_valid_data_return_200(self):
        data = {
            "email": 'robert@gmail.com',
            "password": 'Pass*2024*'
        }
        response = self.client.post('/api/v1/accounts/users/login', data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_request_return_correct_data(self):
        data = {
            "email": 'robert@gmail.com',
            "password": 'Pass*2024*'
        }
        response = self.client.post('/api/v1/accounts/users/login', data=data)
        self.assertEqual(response.data, {
            'user': {
                'id': self.test_user.id,
                'first_name': self.test_user.first_name,
                'last_name': self.test_user.last_name,
                'email': self.test_user.email,
                'mobile_phone': self.test_user.mobile_phone,
                'role': self.test_user.get_role_display(),
                'is_admin_user': self.test_user.is_superuser
            },
            'access_token': response.data.get('access_token'),
            'refresh_token': response.data.get('refresh_token'),
            'token_type': 'Bearer'
        })

    def test_post_request_invalid_user_credentials_email(self):
        data = {
            'email': 'wrongemail@gmail.com',
            'password': 'Pass*2024*'
        }
        response = self.client.post('/api/v1/accounts/users/login', data=data)
        self.assertEqual(response.status_code, 401)

    def test_post_request_invalid_user_credentials_password(self):
        data = {
            'email': 'robert@gmail.com',
            'password': 'wrongpass'
        }
        response = self.client.post('/api/v1/accounts/users/login', data=data)
        self.assertEqual(response.status_code, 401)


class TestListProjectManagerUsers(APITestCase):
    """Test /api/v1/accounts/users/p/ endpoint responses and permissions"""
    def setUp(self):
        self.test_pm_user = User.objects.create_user(email='robert@gmail.com',
                                                     first_name='Robert',
                                                     last_name='Lopez',
                                                     role='P',
                                                     mobile_phone='+53 59876543',
                                                     password='Pass*2024*')

        self.test_pm_user_2 = User.objects.create_user(email='lili@gmail.com',
                                                       first_name='Lili',
                                                       last_name='Tomas',
                                                       role='P',
                                                       mobile_phone='+53 2014783',
                                                       password='Pass*2024*')

        self.test_dev_user = User.objects.create_user(email='jeni@gmail.com',
                                                      first_name='Jeni',
                                                      last_name='Anderson',
                                                      role='D',
                                                      mobile_phone='+1 897456210',
                                                      password='2024-the-year')

        self.test_dev_user_2 = User.objects.create_user(email='bob@gmail.com',
                                                        first_name='Bob',
                                                        last_name='Miles',
                                                        role='D',
                                                        mobile_phone='+1 887540010',
                                                        password='2024-the-year')

        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/accounts/users/p/')
        self.assertEqual(response.status_code, 401)

    def test_get_request_requested_dev_user_authenticated_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/p/')
        self.assertEqual(response.status_code, 403)

    def test_get_request_authenticated_user_returns_200(self):
        response = self.client.get('/api/v1/accounts/users/p/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_authenticated_user_returns_200_and_count_equal_to_2(self):
        response = self.client.get('/api/v1/accounts/users/p/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_request_dont_returns_list_of_non_active_and_deleted_users(self):
        self.test_pm_user = User.objects.create_user(email='camilo@gmail.com',
                                                     first_name='Camilo',
                                                     last_name='Pollock',
                                                     role='P',
                                                     mobile_phone='+1 500008787',
                                                     password='Pass*2024*',
                                                     is_active=False, )

        self.test_pm_user_2 = User.objects.create_user(email='david@gmail.com',
                                                       first_name='David',
                                                       last_name='Chan',
                                                       role='P',
                                                       mobile_phone='+53 209898945',
                                                       password='Pass*2024*',
                                                       deleted=True,
                                                       )
        response = self.client.get('/api/v1/accounts/users/p/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_request_dont_returns_list_of_non_project_manager_users(self):
        self.test_pm_user = User.objects.create_user(email='camilo@gmail.com',
                                                     first_name='Camilo',
                                                     last_name='Pollock',
                                                     role='P',
                                                     mobile_phone='+1 500008787',
                                                     password='Pass*2024*',
                                                     )

        self.test_pm_user_2 = User.objects.create_user(email='david@gmail.com',
                                                       first_name='David',
                                                       last_name='Chan',
                                                       role='D',
                                                       mobile_phone='+53 209898945',
                                                       password='Pass*2024*',
                                                       )
        response = self.client.get('/api/v1/accounts/users/p/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)


class TestListDevelopersUsers(APITestCase):
    """Test /api/v1/accounts/users/d/ endpoint responses and permissions"""

    def setUp(self):
        self.test_pm_user = User.objects.create_user(email='robert@gmail.com',
                                                     first_name='Robert',
                                                     last_name='Lopez',
                                                     role='P',
                                                     mobile_phone='+53 59876543',
                                                     password='Pass*2024*')

        self.test_pm_user_2 = User.objects.create_user(email='lili@gmail.com',
                                                       first_name='Lili',
                                                       last_name='Tomas',
                                                       role='P',
                                                       mobile_phone='+53 2014783',
                                                       password='Pass*2024*')

        self.test_dev_user = User.objects.create_user(email='jeni@gmail.com',
                                                      first_name='Jeni',
                                                      last_name='Anderson',
                                                      role='D',
                                                      mobile_phone='+1 897456210',
                                                      password='2024-the-year')

        self.test_dev_user_2 = User.objects.create_user(email='bob@gmail.com',
                                                        first_name='Bob',
                                                        last_name='Miles',
                                                        role='D',
                                                        mobile_phone='+1 887540010',
                                                        password='2024-the-year')

        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_pm_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/accounts/users/d/')
        self.assertEqual(response.status_code, 401)

    def test_get_request_requested_dev_user_authenticated_returns_403(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_dev_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/d/')
        self.assertEqual(response.status_code, 403)

    def test_get_request_authenticated_user_returns_200(self):
        response = self.client.get('/api/v1/accounts/users/d/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_authenticated_user_returns_200_and_count_equal_to_2(self):
        response = self.client.get('/api/v1/accounts/users/p/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_request_dont_returns_list_of_non_active_and_deleted_users(self):
        self.test_pm_user = User.objects.create_user(email='camilo@gmail.com',
                                                     first_name='Camilo',
                                                     last_name='Pollock',
                                                     role='D',
                                                     mobile_phone='+1 500008787',
                                                     password='Pass*2024*',
                                                     is_active=False, )

        self.test_pm_user_2 = User.objects.create_user(email='david@gmail.com',
                                                       first_name='David',
                                                       last_name='Chan',
                                                       role='D',
                                                       mobile_phone='+53 209898945',
                                                       password='Pass*2024*',
                                                       deleted=True,
                                                       )
        response = self.client.get('/api/v1/accounts/users/d/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_request_dont_returns_list_of_non_dev_users(self):
        self.test_pm_user = User.objects.create_user(email='camilo@gmail.com',
                                                     first_name='Camilo',
                                                     last_name='Pollock',
                                                     role='D',
                                                     mobile_phone='+1 500008787',
                                                     password='Pass*2024*',
                                                     )

        self.test_pm_user_2 = User.objects.create_user(email='david@gmail.com',
                                                       first_name='David',
                                                       last_name='Chan',
                                                       role='P',
                                                       mobile_phone='+53 209898945',
                                                       password='Pass*2024*',
                                                       )
        response = self.client.get('/api/v1/accounts/users/d/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

