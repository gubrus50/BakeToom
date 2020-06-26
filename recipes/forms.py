from django.forms.models import inlineformset_factory
from django import forms
from .models import Recipe, Category
import os



class ContactUsForm(forms.Form):
	TOPIC_CHOICES = (
		('other', 'Inne'),
		('forgot_emai', 'Nie pamiętam adres email'),
		('forgot_username', 'Nie pamiętam nazwy użytkownika'),
		('bug_report', 'Potencjalny błąd strony'),
		('reported_recipe', 'Przepis narusza warunki i usługi'),
		('reported_user', 'Użytkownik narusza warunki i usługi'),
	)

	email = forms.CharField(
		label='Email',
		max_length=150
	)

	topic = forms.ChoiceField(
		choices=TOPIC_CHOICES,
		label='Kategoria',
		initial='',
		required=True,
	)

	message = forms.CharField(
		label='Wiadomość',
		widget=forms.Textarea,
		initial='',
		max_length=10000,
	)

	def send_email(self):
		print('EMAIL HAS BEEN SEND')


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