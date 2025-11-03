from django import forms
from .models import Review
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'user_email', 'phone', 'rating', 'sentiment', 'comment', 'image']
        labels = {
            'product': 'Продукт',
            'user_email': 'Електронна пошта',
            'phone': 'Телефон',
            'rating': 'Оцінка (1-5)',
            'sentiment': 'Настрій відгуку',
            'comment': 'Коментар',
            'image': 'Додати фото',
        }

        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380XXXXXXXXX'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'sentiment': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваш відгук...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image
        max_size_mb = 5
        if image.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f"Розмір зображення не має перевищувати {max_size_mb} MB.")
        content_type = image.content_type
        if content_type not in ('image/jpeg', 'image/png', 'image/webp'):
            raise ValidationError("Дозволені формати: JPEG, PNG, WEBP.")
        return image

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('user_email')
        phone = cleaned.get('phone')
        comment = cleaned.get('comment')
        rating = cleaned.get('rating')

        if not (email or phone or comment or rating):
            raise ValidationError("Вкажіть email, телефон, коментар або рейтинг — принаймні одне поле має бути заповнене.")

        sentiment = cleaned.get('sentiment')
        if rating and sentiment:
            if rating <= 2 and sentiment == 'positive':
                raise ValidationError("Оцінка низька — настрій відгуку не може бути 'Позитивний'.")
            if rating >= 4 and sentiment == 'negative':
                raise ValidationError("Оцінка висока — настрій відгуку не може бути 'Негативний'.")
        return cleaned
