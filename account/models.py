from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

"""ACCOUNT MANAGER"""
class MyAccountManager(BaseUserManager): # overriding what happens when a new user is created
    # required
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        elif not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            email=self.normalize_email(email),# -> converts to lowercase
            username = str(username).lower()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password):
        user = self.create_user(
            email=self.normalize_email(email),# -> converts to lowercase
            username = str(username).lower(),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    # required ends


"""CUSTOM USER MODEL"""
class Account(AbstractBaseUser):
    # required start
    email = models.EmailField(max_length=100,unique=True,verbose_name='email')
    username = models.CharField(max_length=30, unique=True, verbose_name='username')
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # required ends
    
    # additional
    def __str__(self):
        return self.email
    # additional ends

    # django setup
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # django setup ends

    # required starts
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

    # required ends

    # mananger location
    objects = MyAccountManager()
    # manager ends