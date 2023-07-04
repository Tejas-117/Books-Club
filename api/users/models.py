from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
        Custom user model manager where email is the unique identifier for authentication instead of usernames.
    """

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        """
            Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        """
            Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(first_name, last_name, email, password, **extra_fields)


class Tag(models.Model):
   """
      Book 'categories' and User 'interests'.
   """
   text = models.CharField(max_length=100, default=None)

   class Meta:
    db_table = "tags"

   def __str__(self) -> str:
       return self.text



class Gender(models.Model):
    """
        Possible gender values of the user.
    """
    name = models.CharField(max_length=20, default=None)

    class Meta:
        db_table="genders"


class User(AbstractUser):
    """
        Custom User model extending default user.
    """

    # User details
    username = None
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=30, default=None)
    gender = models.ForeignKey(Gender, on_delete=models.SET_DEFAULT, default=4, related_name="gender")
    date_of_birth = models.DateField(blank=True, null=True)

    email = models.EmailField(_('email address'), unique=True)
    password = models.TextField(default=None)

    bio = models.TextField(blank=True, null=True)

    interests = models.ManyToManyField(Tag, related_name="interests")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = CustomUserManager()

    class Meta:
      db_table = 'users'

    def __str__(self):
        return f'{self.first_name}, {self.email}'

    # get all the books listed by the user for exchange.
    def get_exchange_books(self, book_queryset):
        exchange_books = book_queryset.filter(user=self).filter(for_sale = False)
        return exchange_books



class UserImage(models.Model):
    """
        Defines user profile 
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    type = models.CharField(max_length=15, default=None)
    url = models.TextField(default=None)
    filename = models.TextField(default=None)

    class Meta:
        db_table = "user_profile_images"
        constraints = [
            models.CheckConstraint(check=~models.Q(url=""), name="url_required"),
            models.CheckConstraint(
                check=~models.Q(filename=""), name="filename_required"
            ),
            models.CheckConstraint(check=models.Q(type__in=['profile', 'cover']), name="possible_user_image_types")
        ]