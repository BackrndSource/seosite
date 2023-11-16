from django.forms import ModelForm, Textarea, TextInput
from .models import Product, ProductImage, Category, Review, Config


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "title": TextInput(attrs={"size": 100}),
            "slug": TextInput(attrs={"size": 100}),
            "description": Textarea(attrs={"cols": 100, "rows": 5}),
            "meta_description": Textarea(attrs={"cols": 100, "rows": 5}),
        }


class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ConfigForm(ModelForm):
    class Meta:
        model = Config
        fields = "__all__"


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "title": TextInput(attrs={"size": 100}),
            "slug": TextInput(attrs={"size": 100}),
            "description": Textarea(attrs={"cols": 100, "rows": 5}),
            "meta_description": Textarea(attrs={"cols": 100, "rows": 5}),
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        widgets = {
            "title": TextInput(attrs={"size": 100}),
            "author": TextInput(attrs={"size": 100}),
            "text": Textarea(attrs={"cols": 100, "rows": 5}),
        }
