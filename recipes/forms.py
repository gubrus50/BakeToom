from django.forms.models import inlineformset_factory
from django import forms
from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe
		fields = [
			'title',
			'image',
			'recipe_type',
			'description',
			'method',
			'license',
			'nationality',
			'published'
		]

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = [
			'name',
			'ingredients'
		]

CategoriesFormSet = inlineformset_factory(
	Recipe, Category, form=CategoryForm,
	extra=9, can_delete=True, max_num=9
)