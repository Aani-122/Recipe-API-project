"""tests for recipe api"""

from decimal import Decimal
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import (RecipeSerializer,
                                RecipeDetailSerializer,)


RECIPES_URL=reverse("recipe:recipe-list")
def detail_url(receipe_id):
    """create and return recipe detail URL."""
    return reverse('recipe:recipe-detail',args=[receipe_id])

def create_user(**params):
    """create and return new user"""
    return get_user_model().objects.create_user(**params)

def create_recipe(user,**params):
    """create and return sample recipe. """

    defaults={
        'title': "sample recipe title",
        'time_minutes': 22,
        'price': Decimal('5.5'),
        'description':'Sample description',
        'link':" http://how.com",
    }
    defaults.update(params)

    receipe=Recipe.objects.create(user=user,**defaults)
    return receipe

 

class PublicRecipeAPITest(TestCase):
    """test unauthenticated api request"""

    def setUp(self):
        self.client=APIClient()

    def test_auth_required(self):
        """test auth is required to call the API"""
        res=self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """test authorized api request"""

    def setUp(self):
        self.client=APIClient()
        self.user=create_user(email="aniket273@gmail.com",password="password")
        self.client.force_authenticate(self.user)
        #self.token = Token.objects.create(user=self.user)
        #self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_private_recipes(self):
        """test retriving list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res=self.client.get(RECIPES_URL)

        recipes=Recipe.objects.all().order_by('-id')
        serializer=RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_recipe_list_limited_to_uset(self):
        """Test recipes limited to authenticated user"""
        other_user=create_user(email="aniket2yy3@gmail.com",password="password")
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res=self.client.get(RECIPES_URL)

        recipes=Recipe.objects.filter(user=self.user)
        serializer=RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_get_recipe_detail(self):
        recipe=create_recipe(user=self.user)

        url=detail_url(recipe.id)
        res=self.client.get(url)

        serializer=RecipeDetailSerializer(recipe)
        self.assertEqual(res.data,serializer.data)

    def test_create_recipe(self):
        """test creating recipe"""
        payload={
            'title':"samople recipe",
            "time_minutes":5,
            'price':Decimal('40'),
        }

        res=self.client.post(RECIPES_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        
        recipe=Recipe.objects.get(id=res.data['id'])

        for k,v in payload.items():
            self.assertEqual(getattr(recipe,k),v)
        self.assertEqual(recipe.user,self.user)

    def test_partial_update(self):
        """test partial update of recipe"""

        original_link='http://example.com'
        recipe=create_recipe(
            user=self.user,
            title='sample recipe title',
            link=original_link
        )
        payload={"title":"this is new title"}

        url=detail_url(recipe.id)
        res=self.client.patch(url,payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title,payload['title'])
        self.assertEqual(recipe.link,original_link)
        self.assertEqual(recipe.user,self.user)

    def test_update_user_returns_error(self):
        """test changing the user return the error"""

        new_user=create_user(email="user2@example.com",password="passlkfdnk")
        recipe=create_recipe(user=self.user)

        payload={"user":new_user.id}
        url=detail_url(recipe.id)
        self.client.patch(url,payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.user,self.user)

    def test_delete_recipe(self):
        """test deleting recipe sucessfully"""
        recipe=create_recipe(user=self.user)

        url=detail_url(recipe.id)
        res=self.client.delete(url)

        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_users_recipe_error(self):
        """Test trying to delete another user's recipe gives error"""

        new_user=create_user(email="lskdjsk@gmail.com",password="slkdfksaa")
        recipe=create_recipe(user=new_user)

        url=detail_url(recipe.id)
        res=self.client.delete(url)

        self.assertEqual(res.status_code,status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())








    
    
 
