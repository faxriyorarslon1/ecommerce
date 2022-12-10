from django.db import models
from accounts.models import Customer
# Create your models here.

class Category(models.Model):
    name = models.CharField(verbose_name="nomi", max_length=20)
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="nomi", max_length=20)
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.name + "###" + self.category.name

class Product(models.Model):
    name = models.CharField(verbose_name="Nomi", max_length = 30, null=False, blank=False)
    pic = models.ImageField("Rasm", upload_to="product/images/", null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    code = models.CharField("Kod", max_length=10)
    color = models.CharField("Rangi", max_length=10)
    company = models.CharField("Kompaniya nomi", max_length=30)
    info = models.TextField("Umumiy ma'lumot")
    price = models.IntegerField(verbose_name="Narxi", null=False, blank=False)
    amount = models.IntegerField("Miqdori", null=False, blank=False)


    def __str__(self):
        return self.name + "###" + self.category.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Mijoz")
    products = models.ManyToManyField(Product, verbose_name="Maxsulotlar")
    gsum = models.IntegerField(verbose_name="Umumiy summa", null=False, blank=False)
    location = models.CharField("Lokatsiya (Mijoz lokatsiyasi)", max_length=5, null=False, blank=False)
    bonus = models.IntegerField(default=0)
    discount = models.IntegerField(verbose_name="Chegirma", default=0)

    def __str__(self):
        return self.customer.user.first_name + "###" + str(self.gsum)

    


