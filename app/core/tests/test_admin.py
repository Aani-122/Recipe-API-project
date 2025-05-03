"""
test for django admin modifications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client #this is test client which will allow you to create HTTP request. 


class AdminSiteTests(TestCase):
    """Test for django admin ."""

    def setUp(self):
        """ create user and client. """
        self.client = Client() #HTTP requests for testing purpose.
        self.admin_user=get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="test1234",
        )
        self.client.force_login(self.admin_user)
        self.user=get_user_model().objects.create_user(
            email="ani@example.com",
            password="test@1234",
            name="Test user"
        )


    def test_user_list(self):
        """Test that user are listed on page"""

        url=reverse('admin:core_user_changelist')
        res=self.client.get(url)

        self.assertContains(res,self.user.name)
        self.assertContains(res,self.user.email)

    def test_edit_user_page(self):
        """ test the edit user page works"""
        url=reverse("admin:core_user_change",args=[self.user.id])
        res=self.client.get(url)

        self.assertEqual(res.status_code,200)

    def test_create_user_page(self):
        """test create user page working or not """
        url=reverse('admin:core_user_add')
        res=self.client.get(url)

        self.assertEqual(res.status_code,200)
        


