"""
test for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email='user@example.com', password="testpass123"):
    """Create and return new user"""
    return get_user_model().objects.create_user(email,password)

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
    
    def test_create_receipe(self):
        """Test creating a reciepe is sucessful."""

        user=get_user_model().objects.create_user(
            'test@gmail.com',
            'password'
        )

        recipe=models.Recipe.objects.create(
            user=user,
            title='sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='sample test reciepe',
        )

        self.assertEqual(str(recipe),recipe.title)
    
    def test_create_tag(self):
        """Test creating a tag sucessful"""
        user= create_user()
        tag=models.Tag.objects.create(user=user,name='tag1')

        self.assertEqual(str(tag), tag.name)

