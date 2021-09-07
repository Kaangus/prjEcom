import sys
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from django.urls import reverse

User = get_user_model()

def get_product_page_url(obj, viewname, model_name):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})

# Надо сделать функцию, которая будет определять стоимость товара по акции, так же с возможностью выбора
# размера скидки из предложенных (например 10%-20%-30%-50%-80%)
# Так же надо эту функцию надстроить в DiscountProductsManager, чтобы шла сортировка РазмерСкидки/ЦенаТовараПсле

class ResolutionErrorException(Exception):
    pass

class DiscountProductsManager:
    @staticmethod
    def get_discounted_products(*args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.filter(is_discounted=1).order_by('title')
            products.extend(model_products)
        return products


class DiscountProducts:
    objects = DiscountProductsManager()


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
    title = models.CharField(max_length=255, verbose_name="Category title")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (2000, 2000)
    MAX_SIZE = 1048576

    class Meta:
        abstract = True
        ordering = ["title", "is_discounted"]
    title = models.CharField(max_length=255, verbose_name="Product title")
    category = models.ForeignKey(Category, verbose_name="Product category", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Product price")
    image = models.ImageField(upload_to='photos/%y/%m/%d/', verbose_name="Product image", blank=True)
    is_discounted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            image = self.image
            img = Image.open(image)
            min_height, min_width = Product.MIN_RESOLUTION
            max_height, max_width = Product.MAX_RESOLUTION
            if img.height < min_height or img.width < min_width:
                raise ResolutionErrorException("Image is too small( < {}x{})".format(*Product.MIN_RESOLUTION))
            if img.height > max_height or img.width > max_width:
                new_img = img.convert('RGB')
                w_percent = (self.MAX_RESOLUTION[0] / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                resized_new_img = new_img.resize((self.MAX_RESOLUTION[0], h_size), Image.ANTIALIAS)
                filestream = BytesIO()
                resized_new_img.save(filestream, 'JPEG', quality=90)
                filestream.seek(0)
                name = '{}.{}'.format(*self.image.name.split('.'))
                self.image = InMemoryUploadedFile(
                    filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
                )
        super().save(*args, **kwargs)



class Susi(Product):
    class Meta:
        verbose_name = "Susi"
        verbose_name_plural = "Susi"
    type = models.CharField(max_length=255, verbose_name="Susi type")

    def __str__(self):
        return "{} : {}".format(self.category.title, self.title)

    def get_absolute_url(self):
        get_product_page_url(self, 'product_page')

class Pizza(Product):
    class Meta:
        verbose_name = "Pizza"
        verbose_name_plural = "Pizza"
    DOUGH_TYPE = (
        ('T', 'Traditional'),
        ('F', 'Fin'),
    )
    dough = models.CharField(max_length=255, choices=DOUGH_TYPE, verbose_name="Pizza dough type")

    def __str__(self):
        return "{} : {}".format(self.category.title, self.title)

    def get_absolute_url(self):
        get_product_page_url(self, 'product_page')


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name="Cart products owner", on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name="Cart", on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.IntegerField(verbose_name="Cart products quantity")
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Cart products final price")

    def __str__(self):
        return "Product {} in your cart".format(self.content_object.title)


class Cart(models.Model):
    user = models.ForeignKey('Customer', verbose_name="Customer", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    t_qty = models.PositiveIntegerField(default=0, verbose_name="Cart products total quantity")
    f_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Cart products final price")

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name="Customer", on_delete=models.CASCADE)
    p_number = models.CharField(max_length=20, verbose_name="Phone number")
    address = models.CharField(max_length=255, verbose_name="Address")

    def __str__(self):
        return "User: {}".format(self.user.first_name)
