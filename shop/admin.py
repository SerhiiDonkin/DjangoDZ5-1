from django.contrib import admin
from .models import Category, Brand, Ingredient, Manufacturer, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'price', 'stock', 'is_active', 'category', 'brand')
    list_filter = ('is_active', 'category', 'brand')
    search_fields = ('name', 'sku')
    filter_horizontal = ('ingredients',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user_email', 'phone', 'rating', 'sentiment', 'created_at')
    list_filter = ('sentiment', 'rating', 'created_at')
    search_fields = ('user_email', 'phone', 'comment')


