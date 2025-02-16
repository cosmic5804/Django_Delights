from django.urls import path, include
from . import views

urlpatterns = [
    # Home
    path('', views.Index.as_view(), name='index'),
    path("login", include("django.contrib.auth.urls"), name="login"),
    path("logout", views.logout_view, name="logout"),
    # Ingredient Paths
    path('ingredient', views.IngredientView.as_view(), name='ingredient_list'),
    path('ingredient/create', views.IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingredient/<pk>/update', views.IngredientUpdateView.as_view(), name='ingredient_update'),
    path('ingredient/<pk>/delete', views.IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('ingredient/<tk>/requieriment', views.ingredient_requirement_view, name='ingredient_requirement_list'),
    # Menu Item Paths
    path('menu_item', views.MenuItemView.as_view(), name='menu_item_list'),
    path('menu_item/create', views.MenuItemCreateView.as_view(), name='menu_item_create'),
    path('menu_item/<pk>/update', views.MenuItemUpdateView.as_view(), name='menu_item_update'),
    path('menu_item/<pk>/delete', views.MenuItemDeleteView.as_view(), name='menu_item_delete'),
    # Recipe Requirement Paths
    path('menu_item/recipe_requirement/<tk>', views.recipe_requirement_view, name='recipe_requirement_list'),
    path('menu_item/recipe_requirement/<tk>/create', views.RecipeRequirementCreateView.as_view(),
         name='recipe_requirement_create'),
    path('menu_item/recipe_requirement/<tk>/<pk>/update', views.RecipeRequirementUpdateView.as_view(),
         name='recipe_requirement_update'),
    path('menu_item/recipe_requirement/<tk>/<pk>/delete', views.RecipeRequirementDeleteView.as_view(),
         name='recipe_requirement_delete'),
    # Purchase Paths
    path('purchase', views.PurchaseView.as_view(), name='purchase_list'),
    path('purchase/create', views.PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase/<pk>/delete', views.PurchaseDeleteView.as_view(), name='purchase_delete'),
]
