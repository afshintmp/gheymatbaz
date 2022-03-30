from django import forms

from shop.models import Brand, Category, Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'brand']
