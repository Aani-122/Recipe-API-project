"""
test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """test models."""

    def test_create_user_with_email_succesful(self):
        """ Test creatign user with an email sucessfully. """

        email="test@example.com"
        password="testpass123"
        user=get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ test email is normalized for new users."""

        sample_emails=[
            ['test1@EXample.com', "test1@example.com"]
        ]

        for email, excepted in sample_emails:
            user=get_user_model().objects.create_user(email, password='sample123')
            self.assertEqual(user.email,excepted)

    def test_new_user_without_email_raises_error(self):
        " test the user that don't having email "
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(" ",'test123')

    def test_create_super_user(self):
        user=get_user_model().objects.create_superuser(
            'test@example@123',
            'ani123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

