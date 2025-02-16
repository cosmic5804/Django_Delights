from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    KILOGRAM = "kg"
    MILLILITER = "ml"
    LITER = "l"
    GRAM = "gr"
    PIECE = "p"
    METER = "m"
    CUP = "cup"
    OUNCE = "oz"
    UNIT = "u"
    POUND = "lb"
    UNIT_CHOICES = {
        KILOGRAM: "Kilogram",
        MILLILITER: "Milliliter",
        LITER: "Liter",
        GRAM: "Gram",
        PIECE: "Piece",
        METER: "Meter",
        CUP: "Cup",
        OUNCE: "Ounce",
        UNIT: "Unit",
        POUND: "Pound",
    }

    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(choices=UNIT_CHOICES, max_length=3, default=KILOGRAM)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def get_absolute_url():
        return "/ingredient"

    def remove_quantity(self, quantity):
        self.quantity -= quantity
        self.save()


class MenuItem(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.title}'

    @staticmethod
    def get_absolute_url():
        return "/menu_item"

    def can_make_recipe(self):
        for recipe_requirement in self.recipe.all():
            if not recipe_requirement.there_are_ingredient():
                return False
        return True

    def make_recipe(self):
        for recipe_requirement in self.recipe.all():
            recipe_requirement.take_ingredient()

    def recipe_cost(self):
        cost = 0
        for recipe_requirement in self.recipe.all():
            cost += recipe_requirement.cost()
        return cost


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='recipe', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.ingredient}, quantity: {self.quantity}'

    def get_absolute_url(self):
        return reverse('recipe_requirement', kwargs={'tk': self.menu_item})

    def there_are_ingredient(self):
        return True if self.ingredient.quantity >= self.quantity else False

    def take_ingredient(self):
        self.ingredient.remove_quantity(self.quantity)

    def cost(self):
        return self.ingredient.unit_price * self.quantity


class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    profit = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_absolute_url():
        return "/purchase"
