from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.contrib.auth.hashers import make_password


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email :str , password : str, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email : str, password : str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    '''
        Custom Users models 
    '''
    name = models.CharField(("Name of User"), max_length=255)
    mobile_no = models.CharField(max_length=16, unique=True, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    username = None # type : ignore
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    # specify related_name for groups field
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='custom_user_groups'
    )

    # specify related_name for user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='custom_user_permissions'
    )



class UserActivityConstraints(BaseModel):
    '''
        Store constraints threshold here
    '''
    request_limit = models.IntegerField(default=3)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class FriendRequest(BaseModel):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['sender', 'receiver']


class Friendship(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_as_user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_as_friend')

    class Meta:
        unique_together = ['user', 'friend']