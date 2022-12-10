from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField

USER_STATUS_CHOICE =(
    ("Pending", "Pending"),
    ("Active", "Active"),
    ("Deactivated", "Deactivated")
)

USER_ROLE_CHOICE =(
    ("Super Admin", "Super Admin"),
    ("Admin", "Admin"),
    ("Customer", "Customer")
)

class UnverifiedUsers(models.Model):
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    code = models.IntegerField()
    
    def __str__(self) -> str:
        return str(self.phone) +"###"+ str(self.code)
    

class City(models.Model):
    name = models.CharField(verbose_name="Shaxar nomi", max_length=30)

    def __str__(self) -> str:
        return self.name

#Admin and Super Admin
class CustomUser(AbstractUser):
    email = None
    username = models.CharField(_('username'), unique=True, max_length=20)
    pic = models.ImageField(verbose_name="rasm", upload_to="accounts/users/")
    middlename = models.CharField(verbose_name="sharifi", max_length=20)
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    status = models.CharField(choices=USER_STATUS_CHOICE, max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(choices=USER_ROLE_CHOICE, max_length=11)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name


#Customer
class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    discard = models.CharField(max_length=16, verbose_name="Discount karta")
    debt = models.BigIntegerField(verbose_name="qarzi")
    ginfo = models.TextField(verbose_name="Umumiy ma'lumot")

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name









    