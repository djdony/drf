from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
     BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Creates and saves a new user
        if not email:
            raise ValueError('User must have email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Custom user model that support email
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT,
        null=True,
        related_name='profile'
        )
    first_name = models.CharField(max_length=30, blank=True, db_index=True)
    last_name = models.CharField(max_length=30, blank=True, db_index=True)
    address = models.CharField(max_length=150, blank=True)
    whatsapp = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        return
    instance.profile.save()
