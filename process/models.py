from attr.validators import max_len
from django.db import models
from  django.contrib.auth.models import AbstractUser,PermissionsMixin
from .managers import UserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser,PermissionsMixin):
    email = models.EmailField(max_length=100,unique=True,verbose_name='Email')
    first_name = models.CharField(max_length=100, verbose_name=_("first_name"))
    last_name = models.CharField(max_length=100, verbose_name=_("last_name"))
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Returns the user's full name."""
        return f'{self.first_name} {self.last_name}'

class Document(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    file=models.FileField(upload_to='Documents/')
    upload_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,default='uploaded')
    error=models.TextField(default="")

    def __str__(self):
        return self.title

class ExtractedText(models.Model):
    document=models.ForeignKey(Document,on_delete=models.CASCADE)
    text=models.TextField()
    def __str__(self):
        return self.document.title

class AIText(models.Model):
    document=models.ForeignKey(Document,on_delete=models.CASCADE)
    entity=models.JSONField()
    classification=models.JSONField()
    sentiment =models.JSONField()

    def __str__(self):
        return self.document.title