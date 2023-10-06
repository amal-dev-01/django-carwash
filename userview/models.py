from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.


# class CustomUser(AbstractBaseUser):
#     email=models.EmailField(unique=True)
#     mobile=models.CharField(max_length=10)
#     is_active=models.BooleanField(default=False)
    



    # USERNAME_FIELD='email'
    # REQUIRED_FIELDS=['mobile']
    
class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,phone_number,email,password=None):
        if not email:
            raise ValueError('User must have an email address')

        user=self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number
        )
        # user.is_active=True
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin=True
        user.is_active=True
        # user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
    


class UserDetails(AbstractBaseUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=10)
    is_admin=models.BooleanField(default=False)    
    is_staff=models.BooleanField(default=False)    
    is_active=models.BooleanField(default=False)   
    is_superadmin=models.BooleanField(default=False)    
    has_used_coupon = models.BooleanField(default=False)    
    login_failed=models.PositiveIntegerField(default=0)
    is_first_order =  models.BooleanField(default=False)
    
    USERNAME_FIELD='email'
    # REQUIRED_FIELDS=['first_name']
    
    objects=UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    