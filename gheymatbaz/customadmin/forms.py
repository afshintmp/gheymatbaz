from django import forms

from shop.models import Brand, Category, Product, CategoryAttributeValue, CategoryAttribute


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'brand']


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'slug']


class EditeCategory(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = Category
        fields = ['name', 'parent', 'slug']


class CategoryAttributeValueForm(forms.Form):
    attribute_value = forms.CharField()
    parent_attribute_id = forms.ModelChoiceField(queryset=CategoryAttribute.objects.all(), widget=forms.HiddenInput)

    # class Meta:
    #     model = Cat
