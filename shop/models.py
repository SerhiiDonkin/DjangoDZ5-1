from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


# from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name or f"Категорія #{self.pk}"


class Brand(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"

    def __str__(self):
        return self.name or f"Бренд #{self.pk}"


class Ingredient(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Інгредієнт"
        verbose_name_plural = "Інгредієнти"

    def __str__(self):
        return self.name or f"Інгредієнт #{self.pk}"


class Manufacturer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Виробник"
        verbose_name_plural = "Виробники"

    def __str__(self):
        return self.name or f"Виробник #{self.pk}"


class Product(models.Model):
    sku = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='products')

    ingredients = models.ManyToManyField(Ingredient, blank=True, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"

    def __str__(self):
        return self.name or f"Продукт #{self.pk}"


class Review(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Позитивний'),
        ('negative', 'Негативний'),
    ]

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Продукт'))

    user_email = models.EmailField(
        verbose_name=_('Електронна пошта'),
        blank=True, null=True
    )
    phone = models.CharField(
        verbose_name=_('Телефон'),
        max_length=20,
        blank=True, null=True,
        validators=[RegexValidator(r'^\+?\d{7,15}$', message='Введіть телефон у форматі +380... або 095...')]
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name=_('Оцінка'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True, null=True
    )
    sentiment = models.CharField(
        verbose_name=_('Негатив/Позитив'),
        max_length=8,
        choices=SENTIMENT_CHOICES,
        blank=True,
        null=True
    )
    comment = models.TextField(verbose_name=_('Коментар'), blank=True, null=True)
    image = models.ImageField(verbose_name=_('Зображення'), upload_to='reviews/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    def __str__(self):
        return f"Відгук #{self.pk} — {self.product.name if self.product else 'без продукту'}"
