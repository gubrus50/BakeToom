from django import forms
from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe
		fields = [
			'title',
			'image',
			'description',
			'method'
		]

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = [
			'name',
			'ingredients'
		]

