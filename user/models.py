from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
           

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    fullname = models.CharField(db_column='Full Name',max_length=100)
    contact = models.CharField(db_column='Contact',max_length=100)
    city = models.CharField(db_column='City',max_length=100)
    image = models.ImageField(db_column='Profile Picture',upload_to='images')
    gpa = models.ImageField(db_column='gpa Picture',upload_to='gpa',null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    gpa_status = models.BooleanField(default=False)
    point1 = models.CharField(max_length=10,null=True)
    point2 = models.CharField(max_length=10,null=True)
    point3 = models.CharField(max_length=10,null=True)
    point4 = models.CharField(max_length=10,null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        db_table = 'User'



class Profile(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)
    forget_token = models.CharField(max_length=1000)
    class Meta:
        db_table = 'Forget_password'

class otp_m(models.Model):
    otp_set = models.IntegerField()
    class Meta:
        db_table = 'otp'