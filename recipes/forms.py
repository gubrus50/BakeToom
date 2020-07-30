from django.forms.models import inlineformset_factory
from django import forms
from .models import Recipe, Category
import os



class ContactUsForm(forms.Form):
	TOPIC_CHOICES = (
		('other',          'Inne'),
		('auth_failure',   'Nie mogę dostać się do mojego konta'),
		('forgot_email',   'Nie pamiętam mojego adresu email'),
		('forgot_username','Nie pamiętam nazwy użytkownika'),
		('impersonation',  'Ktoś podszywa się pode mnie'),
		('user_claim',     'Użytkownik narusza warunki i usługi'),
		('user_claim',     'Użytkownik rozprowadza mój przepis bez mojej zgody'),
		('recipe_claim',   'Przepis narusza warunki i usługi'),
		('recipe_claim',   'Przepis narusza prawa autorskie'),
		('bug_report',     'Potencjalny błąd strony')
	)

	email = forms.CharField(
		label='Email',
		max_length=150
	)

	subject = forms.ChoiceField(
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