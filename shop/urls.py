from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.ishop, name='shop'),
    path('product/<int:product_id>/review/', views.submit_review, name='submit_review_for_product'),
    path('review/submit/', views.submit_review, name='submit_review'),
]
