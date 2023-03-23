from django.forms.models import inlineformset_factory
from django import forms
from .models import Recipe, Category
from captcha.fields import ReCaptchaField


class ContactUsForm(forms.Form):
	TOPIC_CHOICES = (
		('other',          'Other'),
		('auth_failure',   'I can\'t access my account'),
		('forgot_email',   'I don\'t remember my email address'),
		('forgot_username','I don\'t remember my username'),
		('impersonation',  'Someone is impersonating me'),
		('user_claim',     'The user violates the terms and services'),
		('user_claim',     'A user distributes my recipe without my consent'),
		('recipe_claim',   'The recipe violates terms and services'),
		('recipe_claim',   'The recipe violates copyright'),
		('bug_report',     'Potential page error')
	)

	email = forms.CharField(
		label='Email',
		max_length=150
	)

	subject = forms.ChoiceField(
		choices=TOPIC_CHOICES,
		initial='',
		required=True,
	)

	message = forms.CharField(
		widget=forms.Textarea,
		initial='',
		max_length=10000,
	)

	captcha = ReCaptchaField()


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