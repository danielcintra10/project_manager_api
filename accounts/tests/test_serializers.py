from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from api.serializers import UserSerializer, MyTokenObtainPairSerializer

User = get_user_model()


class TestUserSerializer(TestCase):
    """Test UserSerializer to check if works properly"""

    def setUp(self):
        self.test_user = User.objects.create_user(email='robert@gmail.com',
                                                  first_name='Robert',
                                                  last_name='Lopez',
                                                  role='D',
                                                  mobile_phone='+53 59876543',
                                                  password='strongpass2024')

    def test_serialize_user_data_ok(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        serializer = UserSerializer(user, many=False)
        self.assertEqual('Robert', serializer.data.get("first_name"))
        self.assertEqual('Lopez', serializer.data.get("last_name"))
        self.assertEqual('robert@gmail.com', serializer.data.get("email"))
        self.assertEqual('D', serializer.data.get("role"))
        self.assertEqual('+53 59876543', serializer.data.get("mobile_phone"))
        self.assertTrue("password" not in serializer.data)
        self.assertTrue(serializer.data.get("is_active"))
        self.assertTrue("is_super_user" not in serializer.data)
        self.assertTrue("creation_date" in serializer.data)
        self.assertTrue("last_update" in serializer.data)
        self.assertTrue("id" in serializer.data)

    def test_deserialize_valid_user_object(self):
        serialized_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "mobile_phone": "+1 123456789",
            "role": "D",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        user = serializer.save()
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.role, "D")
        self.assertEqual(user.mobile_phone, "+1 123456789")
        # Check if password is encrypted correctly
        self.assertTrue(user.check_password("StrongPassword123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_update_valid_user_object_no_partial_data(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        updated_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "mobile_phone": "+1 123456789",
            "role": "P",
            "password": "Pass78*80",
        }
        serializer = UserSerializer(instance=user, data=updated_data, partial=False)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.role, "P")
        self.assertEqual(user.mobile_phone, "+1 123456789")
        # Check if password is encrypted correctly
        self.assertTrue(user.check_password("Pass78*80"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_update_valid_user_object_with_partial_data(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        updated_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
        }
        serializer = UserSerializer(instance=user, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        # Fields updated
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        # Fields with old data
        self.assertEqual(user.role, "D")
        self.assertEqual(user.mobile_phone, "+53 59876543")
        # Check if password is encrypted correctly
        self.assertTrue(user.check_password("strongpass2024"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_can_update_password(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        updated_data = {
            "password": "Password/new01/**",
        }
        serializer = UserSerializer(instance=user, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password("Password/new01/**"))

    def test_validation_error_weak_password(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        updated_data = {
            "password": "1234",
        }
        serializer = UserSerializer(instance=user, data=updated_data, partial=True)
        self.assertFalse(serializer.is_valid())

    def test_read_only_fields_not_when_deserialize(self):
        serialized_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "mobile_phone": "+1 123456789",
            "role": "D",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        with self.assertRaises(KeyError):
            id = serializer.validated_data["id"]
            is_active = serializer.validated_data["is_active"]
            creation_date = serializer.validated_data["creation_date"]
            last_update = serializer.validated_data["last_update"]

    def test_save_user_object_with_correct_fields(self):
        serialized_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "mobile_phone": "+1 123456789",
            "role": "D",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        user = User.objects.filter(email__exact='johndoe@example.com').first()
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.role, "D")
        self.assertEqual(user.mobile_phone, "+1 123456789")
        # Check if password is encrypted correctly
        self.assertTrue(user.check_password("StrongPassword123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_validation_error_non_unique_email(self):
        serialized_data = {
            "first_name": "John",
            "last_name": "Doe",
            # This email already exist
            "email": "robert@gmail.com",
            "mobile_phone": "+1 123456789",
            "role": "D",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(data=serialized_data)
        self.assertFalse(serializer.is_valid())

    def test_validation_error_non_unique_phone_number(self):
        serialized_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            # This mobile_phone already exist
            "mobile_phone": "+53 59876543",
            "role": "D",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(data=serialized_data)
        self.assertFalse(serializer.is_valid())

    def test_validation_error_email_wrong_format(self):
        serialized_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe",
            # This mobile_phone already exist
            "mobile_phone": "59876543RTY**",
            "role": "D",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(data=serialized_data)
        self.assertFalse(serializer.is_valid())

    def test_validation_error_names_with_numbers_and_special_chars(self):
        serialized_data = {
            "first_name": "8911",
            "last_name": "+89Polo",
            "email": "johndoe@example.com",
            # This mobile_phone already exist
            "mobile_phone": "+53 59876543",
            "role": "D",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(data=serialized_data)
        self.assertFalse(serializer.is_valid())

    def test_validation_error_mobile_phone_with_letters(self):
        serialized_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            # This mobile_phone already exist
            "mobile_phone": "59876543RTY**",
            "role": "D",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(data=serialized_data)
        self.assertFalse(serializer.is_valid())


class TestMyTokenObtainPairSerializer(TestCase):
    """Test MyTokenObtainPairSerializer to check if works properly"""

    def setUp(self):
        self.test_user = User.objects.create_user(email='robert@gmail.com',
                                                  first_name='Robert',
                                                  last_name='Lopez',
                                                  role='D',
                                                  mobile_phone='+53 59876543',
                                                  password='Pass*2024*')

    def test_validate_method_returns_expected_data_representation(self):
        serializer = MyTokenObtainPairSerializer()
        attrs = {'email': 'robert@gmail.com', 'password': 'Pass*2024*'}

        result = serializer.validate(attrs)

        assert 'user' in result
        assert 'access_token' in result
        assert 'refresh_token' in result
        assert 'token_type' in result
        assert result['token_type'] == 'Bearer'

    def test_invalid_credentials_raise_authentication_failed_error(self):
        serializer = MyTokenObtainPairSerializer()
        attrs = {'email': 'invaliduser', 'password': 'invalidpassword'}

        with self.assertRaises(AuthenticationFailed):
            serializer.validate(attrs)

    def test_missing_credentials_raise_key_error(self):
        serializer = MyTokenObtainPairSerializer()
        attrs = {}

        with self.assertRaises(KeyError):
            serializer.validate(attrs)

    def test_user_object_correctly_serialized_in_data_representation(self):
        serializer = MyTokenObtainPairSerializer()
        attrs = {'email': 'robert@gmail.com', 'password': 'Pass*2024*'}

        result = serializer.validate(attrs)

        assert 'user' in result
        assert 'id' in result['user']
        assert 'first_name' in result['user']
        assert 'last_name' in result['user']
        assert 'email' in result['user']
        assert 'mobile_phone' in result['user']
        assert 'role' in result['user']
        assert 'is_admin_user' in result['user']

    def test_correct_data_in_serializer_data(self):
        serializer = MyTokenObtainPairSerializer()
        attrs = {'email': 'robert@gmail.com', 'password': 'Pass*2024*'}

        data = serializer.validate(attrs)
        self.assertEqual(data.get("user").get("first_name"), "Robert")
        self.assertEqual(data.get("user").get("last_name"), "Lopez")
        self.assertEqual(data.get("user").get("email"), "robert@gmail.com")
        self.assertEqual(data.get("user").get("role"), "Developer")
        self.assertEqual(data.get("user").get("mobile_phone"), "+53 59876543")
        self.assertEqual(data.get("user").get("is_admin_user"), False)
        self.assertEqual(data.get("token_type"), "Bearer")
