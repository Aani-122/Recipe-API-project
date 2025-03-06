'''

database models.
'''

from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class Usermanager(BaseUserManager):
    """ manager for user. """
    def create_user(self, email, password=None, **extra_fields):
        """create save and return new user"""
        if not email or email==" ":
            raise ValueError("user must have email address")
        user=self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,email,password):
        """create and return a new user."""
        user=self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True 
        user.save(using=self._db)

        return user



class User(AbstractBaseUser, PermissionsMixin):
    """user in the system. """
    email=models.EmailField(max_length=255, unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=Usermanager()

    USERNAME_FIELD= 'email'



# Create your models here.
