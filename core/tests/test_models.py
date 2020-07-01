from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        # Test Creating user with email
        email = 'test@test.com'
        password = 'test'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        # Normalize Email
        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(email, 'password')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'password')

    def test_create_superuser(self):
        # Test Creating new Superuser
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'password'
            )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
