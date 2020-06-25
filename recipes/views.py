from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin
)
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	DeleteView,
	CreateView
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction
from django.db.models import F, Q
from datetime import datetime, timedelta
from .models import Recipe, Category
from .forms import (
	RecipeForm,
	CategoryForm,
	CategoriesFormSet
)
import os, base64, requests




class RecipeListView(ListView):
	model = Recipe
	template_name = 'recipes/home.html'
	context_object_name = 'recipes'
	paginate_by = 32

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['query'] = self.request.GET.get('q', '')
		return context


	def get_queryset(self):
		query 				= self.request.GET.get('q', '')
		recipe_title 		= self.request.GET.get('title')
		publisher 			= self.request.GET.get('publisher')
		certified 			= self.request.GET.get('certified')
		recipe_id 			= self.request.GET.get('id')
		search_by_date 		= self.request.GET.get('search_by_date')
		recipe_type 		= self.request.GET.get('type')
		nationality_mode 	= self.request.GET.get('nationality_mode')
		nationality			= self.request.GET.get('nationality')



		query_set = Q()
		query_set &= Q(published=True)

		if query:
			if recipe_title:
				query_set &= Q(title__icontains=query)

			if publisher:
				query_set |= Q(publisher__username__icontains=query)

			if recipe_id:
				try:
					int(query)
				except:
					# Id must be an integer.
					messages.error(self.request, f'ERROR - Identyfikator musi być liczbą całkowitą.')
				else:
					query_set |= Q(id__exact=query)

		if certified:
			query_set &= Q(certified=True)

		if recipe_type and recipe_type != 'general':
			query_set &= Q(recipe_type__iexact=recipe_type)

		if nationality_mode == 'specific' and nationality:
			query_set &= Q(nationality__iexact=nationality)

		elif nationality_mode == 'international':
			query_set &= Q(nationality__iexact='')

		# general upload date
		if search_by_date and search_by_date != 'GUD':
			t = timezone.localtime(timezone.now())

			# today's upload date
			if search_by_date == 'TUD':
				query_set &= Q(date_posted__day=t.day)
				query_set &= Q(date_posted__month=t.month)
				query_set &= Q(date_posted__year=t.year)

			# this week upload date
			elif search_by_date == 'TWUD':
				week_start = datetime.today()
				week_start -= timedelta(days=week_start.weekday())
				week_end = week_start + timedelta(days=7)
				query_set &= Q(date_posted__gte=week_start)
				query_set &= Q(date_posted__lt=week_end)
				query_set &= Q(date_posted__month=t.month)
				query_set &= Q(date_posted__year=t.year)

			# this month upload date
			elif search_by_date == 'TMUD':
				query_set &= Q(date_posted__month=t.month)
				query_set &= Q(date_posted__year=t.year)

			# this year upload date
			elif search_by_date == 'TYUD':
				query_set &= Q(date_posted__year=t.year)

			# date of creation
			elif search_by_date == 'DOC' and query:
				date = None
				try:
					datetime.strptime(query, '%d/%m/%Y')
				except:
					try:
						datetime.strptime(query, '%d-%m-%Y')
					except:
						# Invalid data form error.
						messages.error(self.request, f'ERROR - Wprowadzona data musi być ułożona w następującej formie - DD/MM/YYYY.')
					else:
						date = datetime.strptime(query, '%d-%m-%Y')
				else:
					date = datetime.strptime(query, '%d/%m/%Y')

				if date:
					query_set &= Q(date_created__date=date)




		if len(query_set) == 1:
			object_list = self.model.objects.filter(query_set).order_by(F('title').asc(nulls_last=True))
		else:
			object_list = self.model.objects.filter(query_set).order_by(F('title').asc(nulls_last=True))

		return object_list





class UserRecipeListView(ListView):
	model = Recipe
	template_name = 'recipes/user_recipes.html'
	context_object_name = 'recipes'
	paginate_by = 32

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		query = self.request.GET.get('q')
		
		if query:
			# Order by title, and move null values to last position.
			object_list = self.model.objects.filter(publisher=user, title__icontains=query).order_by(F('title').asc(nulls_last=True))
		else:
			# Order by title, and move null values to last position.
			object_list = self.model.objects.filter(publisher=user).order_by(F('title').asc(nulls_last=True))
		return object_list





class RecipeDetailView(DetailView):
	model = Recipe
	def get_context_data(self, **kwargs):
		recipe_id = self.kwargs['pk']
		context = super(RecipeDetailView, self).get_context_data(**kwargs)
		context['categories'] = Category.objects.select_related().filter(recipe=recipe_id)
		return context





class RecipePlainView(DetailView):
	model = Recipe
	template_name = 'recipes/recipe_plain.html'

	def get_context_data(self, **kwargs):
		context = super(RecipePlainView, self).get_context_data(**kwargs)
		context['categories'] = Category.objects.all()

		url = self.object.image.url
		r = requests.get(url)
		if r.status_code == 200:
			byteBase64 = base64.b64encode(requests.get(url).content)
			context['recipe_image_base64'] = byteBase64.decode("utf-8")
		else:
			context['recipe_image_base64'] = False
		
		return context





class RecipeCreateView(LoginRequiredMixin, CreateView):
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


	def get_context_data(self, **kwargs):
		data = super(RecipeCreateView, self).get_context_data(**kwargs)
		data['on_update_view'] = False
		data['categories_max_num'] = CategoriesFormSet.max_num
		data['categories_name_label'] = Category._meta.get_field('name').verbose_name
		data['categories_ingredients_label'] = Category._meta.get_field('ingredients').verbose_name 


		if self.request.POST:
			data['categories'] = CategoriesFormSet(self.request.POST)
		else:
			data['categories'] = CategoriesFormSet()
		return data


	def form_valid(self, form):
		context = self.get_context_data()
		categories = context['categories']

		with transaction.atomic():
			form.instance.publisher = self.request.user
			self.object = form.save()
		
			if categories.is_valid():
				categories.instance = self.object
				categories.save()

		return super(RecipeCreateView, self).form_valid(form)


	def get_success_url(self):
		messages.success(self.request, f'Twój przepis został pomyślnie utworzony.')
		return reverse_lazy('recipe-detail', kwargs={'pk': self.object.pk})





class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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


	def get_context_data(self, **kwargs):
		data = super(RecipeUpdateView, self).get_context_data(**kwargs)
		data['on_update_view'] = True
		data['categories_max_num'] = CategoriesFormSet.max_num
		data['categories_name_label'] = Category._meta.get_field('name').verbose_name
		data['categories_ingredients_label'] = Category._meta.get_field('ingredients').verbose_name 


		if self.request.POST:
			data['categories'] = CategoriesFormSet(self.request.POST, instance=self.object)
		else:
			data['categories'] = CategoriesFormSet(instance=self.object)
		return data


	def test_func(self):
		recipe = self.get_object()
		if self.request.user == recipe.publisher:
			return True
		return False


	def form_valid(self, form):
		context = self.get_context_data()
		categories = context['categories']

		with transaction.atomic():
			form.instance.publisher = self.request.user
			self.object = form.save()
		
			if categories.is_valid():
				categories.instance = self.object
				categories.save()

		return super(RecipeUpdateView, self).form_valid(form)


	def get_success_url(self):
		messages.success(self.request, f'Twój przepis został pomyślnie zaktualizowany.')
		return reverse_lazy('recipe-detail', kwargs={'pk': self.object.pk})





class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Recipe
	success_url = '/'
	success_message = 'Your recipe has been successfully removed.'

	def test_func(self):
		recipe = self.get_object()
		if self.request.user == recipe.publisher:
			return True
		return False

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(RecipeDeleteView, self).delete(request, *args, **kwargs)
	




def AboutView(request):
	return render(request, 'recipes/about.html')

def TermsAndConditions(request):
	return render(request, 'recipes/terms_and_conditions_pl.html')

def PrivacyAndPolicy(request):
	return render(request, 'recipes/privacy_and_policy_pl.html')

def ContactUsForm(request):
	context = {
		'BAKETOOM_MAIL_USER': os.environ.get('BAKETOOM_MAIL_USER')
	}
	return render(request, 'recipes/contact_us_form.html', context)