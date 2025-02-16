from django import forms
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit', 'unit_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingredient'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity', 'step': '0.01'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'step': '0.01'}),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'step': '0.01'}),
        }


class RecipeRequirementForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = RecipeRequirement
        fields = ['ingredient', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity', 'step': '0.01'}),
        }


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['menu_item']
        widgets = {
            'menu_item': forms.Select(attrs={'class': 'form-select'}),
        }
