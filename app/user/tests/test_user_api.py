"""
tests for user Api
"""

from django.test import TestCase
from django.contrib.auth  import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL= reverse('user:create')
TOKEN_URL= reverse('user:token')
ME_URL=reverse('user:me')

def create_user(**params):
    """create and return a new user"""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """test the public feature for the user api """

    def setUp(self):
        self.client=APIClient()

    def test_create_user_success(self):
        """test creating user successful. """
        payload={
            'email':"test@example.com",
            'password': "testpss123",
            'name':"aniket"
        }
        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user=get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_with_emai_exist_error(self):
        "testing for already existing email address"
        payload={
            'email':"testexample.com",
            'password': "testpss123",
            'name':"aniket patil"
        }
        create_user(**payload)
        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 char"""
        payload={
            'email':"testexample.com",
            'password': "tes",
            'name':"aniket patil"
        }
        res=self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists=get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)
    
    def test_create_token_for_user(self):
        """test generate token for valid credentials """
        user_details={
            'name': "Test name",
            "email": "test@example.com",
            "password": "aniket"
        }
        create_user(**user_details)
        payload={
            'email':user_details['email'],
            'password': user_details['password']
        }
        res=self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return if credentials invalid."""
        create_user(email="aniket@email.com",password="goodpass")
        payload={
            "email":"aniket@email.com",
            "password":"badpass"
        }
        res=self.client.post(TOKEN_URL,**payload)  #this will return the data with the token 

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """test posting blank password return error"""
        payload={
            "email":"aniket@emial.com",
            "password":" "
        }
        res=self.client.post(TOKEN_URL,**payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_retrive_user_unathorised(self):
        """test authentication is required for the users"""

        res=self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """test api request that require authentication."""

    def setUp(self):
        self.user=create_user(
            email="test@emaple.com",
            password='anfsoajf',
            name='aniket',
        )

        self.client=APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_reterive_profile_sucess(self):
        """test retriving profile for logged in user"""
        res=self.client.get(ME_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)

        self.assertEqual(res.data,{
            "email":self.user.email,
            "name":self.user.name,
        })

    def test_post_me_not_allowed(self):
        """test POST is not allowed in the me endpoint"""
        res=self.client.post(ME_URL,{})
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticate user """

        payload={'name':"testn ame",'password':"sjhgjfsdd"}
        res=self.client.patch(ME_URL,payload)

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code,status.HTTP_200_OK)



    

        




