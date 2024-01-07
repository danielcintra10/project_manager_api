from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

User = get_user_model()


class TestUser(TestCase):
    """Test User model to check work properly"""

    def setUp(self):
        self.test_user = User.objects.create_user(email='robert@gmail.com',
                                                  first_name='Robert',
                                                  last_name='Lopez',
                                                  role='D',
                                                  mobile_phone='+53 59876543',
                                                  password='1234')

        self.test_super_user = User.objects.create_superuser(email='dany@gmail.com',
                                                             first_name='Daniel',
                                                             last_name='Lopez',
                                                             role='D',
                                                             mobile_phone='+53 54876543',
                                                             password='fcb')

    def test_password_is_correct_encrypted(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        assert user.check_password('1234') is True

    def test_password_is_correct_encrypted_in_super_user(self):
        user = User.objects.filter(email__exact='dany@gmail.com').first()
        assert user.check_password("fcb") is True

    def test_user_can_update_password(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        user.set_password("danyfcb10")
        user.save()
        assert user.check_password('danyfcb10') is True

    def test_update_user_with_partial_fields_do_not_affect_password(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        user.email = 'dany.webd3v@gmail.com'
        user.first_name = 'Daniel'
        user.role = 'P'
        user.save()
        # Verify that a new user was not created and the existing one is updated.
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(user.email, 'dany.webd3v@gmail.com')
        self.assertEqual(user.first_name, 'Daniel')
        self.assertEqual(user.role, 'P')
        # Verify that the update don't affect the password.
        assert user.check_password('1234') is True

    def test_create_new_user_with_valid_data(self):
        new_user = User.objects.create(email='migue@gmail.com',
                                       first_name='Miguel',
                                       last_name='Perez',
                                       role='D',
                                       mobile_phone='+53 51234567',
                                       password='password123')
        user = User.objects.filter(email__exact='migue@gmail.com').first()
        data = {'email': 'migue@gmail.com',
                'first_name': 'Miguel',
                'last_name': 'Perez',
                'role': 'D',
                'mobile_phone': '+53 51234567',
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
                'deleted': False,
                }
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(data, {'email': user.email,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'role': user.role,
                                'mobile_phone': user.mobile_phone,
                                'is_active': user.is_active,
                                'is_staff': user.is_staff,
                                'is_superuser': user.is_superuser,
                                'deleted': user.deleted,
                                })

    def test_error_when_create_a_user_with_missing_fields(self):
        with self.assertRaises(Exception):
            new_user = User.objects.create(email='migue@gmail.com',
                                           first_name='Miguel',
                                           last_name='Perez',
                                           )

    def test_delete_user(self):
        new_user = User.objects.create(email='migue@gmail.com',
                                       first_name='Miguel',
                                       last_name='Perez',
                                       role='D',
                                       mobile_phone='+53 51234567',
                                       password='password123')
        self.assertEqual(User.objects.count(), 3)
        new_user.delete()
        self.assertEqual(User.objects.count(), 2)
        self.assertFalse(User.objects.filter(email__exact='migue@gmail.com').exists())

    def test_database_return_correct_user_looking_for_email_field(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        self.assertEqual(user, self.test_user)

    def test_validate_email_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            new_user = User.objects.create(email='robert@gmail.com',
                                           first_name='Miguel',
                                           last_name='Perez',
                                           role='D',
                                           mobile_phone='+53 51234567',
                                           password='password123')

    def test_validate_mobile_phone_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            new_user = User.objects.create(email='email@example.com',
                                           first_name='Miguel',
                                           last_name='Perez',
                                           role='D',
                                           mobile_phone='+53 59876543',
                                           password='password123')

    def test_update_user_with_invalid_email_format(self):
        with self.assertRaises(ValidationError):
            self.test_user.email = 'email'
            self.test_user.full_clean()
            self.test_user.save()

    def test_update_user_with_non_numeric_characters_in_mobile_phone_(self):
        with self.assertRaises(ValidationError):
            self.test_user.mobile_phone = '+000 590020aaa&'
            self.test_user.full_clean()
            self.test_user.save()

    def test_update_user_with_numbers_or_simbols_in_first_name(self):
        with self.assertRaises(ValidationError):
            self.test_user.first_name = 'pedro123'
            self.test_user.full_clean()
            self.test_user.save()

    def test_update_user_with_numbers_or_simbols_in_last_name(self):
        with self.assertRaises(ValidationError):
            self.test_user.last_name = '$%78Torres'
            self.test_user.full_clean()
            self.test_user.save()

    def test_create_new_user_with_different_roles_than_P_or_D(self):
        with self.assertRaises(ValidationError):
            new_user = User(email='migue@gmail.com',
                            first_name='Miguel',
                            last_name='Perez',
                            role='Y',
                            mobile_phone='+53 51234567',
                            password='password123')
            new_user.full_clean()
            new_user.save()
