from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm, PurchaseForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Home
def logout_view(request):
    logout(request)
    return redirect("index")


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/index.html'


# Ingredient Views
class IngredientView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredient.html"


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/add_ingredient.html"
    form_class = IngredientForm


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/update_ingredient.html"
    form_class = IngredientForm
    success_url = "/ingredient"


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/delete_ingredient.html"
    success_url = "/ingredient"


@login_required
def ingredient_requirement_view(request, tk):
    menu = MenuItem.objects.get(id=tk)
    recipe_requirements = menu.recipe.all()
    ingredients = [recipe_requirement.ingredient for recipe_requirement in recipe_requirements]
    requirement_ingredients = zip(ingredients, recipe_requirements)
    context = {
        'menu': menu,
        'requirement_ingredients': requirement_ingredients,
    }
    return render(request, "inventory/ingredient_requirement.html", context)


# Menu Item Views
class MenuItemView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/menu_item.html"


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = "inventory/add_menu_item.html"
    form_class = MenuItemForm


class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    template_name = "inventory/update_menu_item.html"
    form_class = MenuItemForm
    success_url = "/menu_item"


class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "inventory/delete_menu_item.html"
    success_url = "/menu_item"


@login_required
def recipe_requirement_view(request, tk):
    menu = get_object_or_404(MenuItem, pk=tk)
    recipe_requirements = menu.recipe.all()
    context = {
        "menu": menu,
        "recipe_requirements": recipe_requirements,
    }
    return render(request, 'inventory/recipe_requirement.html', context)


class RecipeRequirementCreateView(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = 'inventory/add_recipe_requirement.html'
    form_class = RecipeRequirementForm

    def get_initial(self):
        tk = self.kwargs.get('tk')
        menu_item = MenuItem.objects.get(id=tk)
        initial = super().get_initial()
        initial['menu_item'] = menu_item
        return initial

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        tk = self.kwargs.get('tk')
        contex['menu_item'] = MenuItem.objects.get(id=tk)
        return contex

    def get_success_url(self):
        tk = self.kwargs['tk']
        return reverse_lazy('recipe_requirement_list', kwargs={'tk': tk})

    def form_valid(self, form):
        menu_item = MenuItem.objects.get(id=self.kwargs['tk'])
        form.instance.menu_item = menu_item
        return super().form_valid(form)


class RecipeRequirementUpdateView(LoginRequiredMixin, UpdateView):
    model = RecipeRequirement
    template_name = 'inventory/update_recipe_requirement.html'
    form_class = RecipeRequirementForm

    def get_success_url(self):
        tk = self.kwargs['tk']
        return reverse_lazy('recipe_requirement_list', kwargs={'tk': tk})

    def form_valid(self, form):
        menu_item = MenuItem.objects.get(id=self.kwargs['tk'])
        form.instance.menu_item = menu_item
        return super().form_valid(form)


class RecipeRequirementDeleteView(LoginRequiredMixin, DeleteView):
    model = RecipeRequirement
    template_name = 'inventory/delete_recipe_requirement.html'

    def get_success_url(self):
        tk = self.kwargs['tk']
        return reverse_lazy('recipe_requirement_list', kwargs={'tk': tk})


class PurchaseView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchase.html"


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = "inventory/add_purchase.html"
    form_class = PurchaseForm

    def form_valid(self, form):
        menu_item = form.instance.menu_item
        if not menu_item.can_make_recipe():
            return HttpResponseRedirect(reverse_lazy('ingredient_requirement_list', kwargs={'tk': menu_item.id}))
        form.instance.revenue = menu_item.price
        form.instance.cost = round(menu_item.recipe_cost(), 2)
        form.instance.profit = round(menu_item.price - menu_item.recipe_cost(), 2)

        menu_item.make_recipe()
        return super().form_valid(form)


class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = "inventory/delete_purchase.html"
    success_url = "/purchase"
