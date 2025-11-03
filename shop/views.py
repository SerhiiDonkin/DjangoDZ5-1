from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReviewForm
from .models import Product

def ishop(request):
    return HttpResponse("shop")

def submit_review(request, product_id=None):
    """
    Якщо product_id передано — підставляємо product у форму.
    """
    initial = {}
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        initial['product'] = product
    else:
        product = None

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save()
            messages.success(request, f"Відгук для продукту {review.product.name} успішно додано!")
            if product:
                return redirect('product_detail', pk=product.pk)
            return redirect('reviews_thanks')
        else:
            messages.error(request, "Будь ласка, виправте помилки у формі.")
    else:
        form = ReviewForm(initial=initial)

    return render(request, 'shop/review_form.html', {'form': form, 'product': product})