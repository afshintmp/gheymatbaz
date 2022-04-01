from django import forms

from shop.models import Brand, Category, Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'brand']


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'slug']


class EditeCategory(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Category
        fields = ['name', 'parent', 'slug']
