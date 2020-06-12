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
	DeleteView
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import F, Q
from datetime import datetime, timedelta
from .models import Recipe, Category
from .forms import RecipeForm, CategoryForm
import os, base64, requests




class RecipeListView(ListView):
	model = Recipe
	template_name = 'recipes/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'recipes'
	paginate_by = 12

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

		if search_by_date and search_by_date != 'GUD':
			t = timezone.localtime(timezone.now())

			# today's upload date
			if search_by_date == 'TUD':
				query_set &= Q(date_posted__day=t.day)

			# this week upload date
			elif search_by_date == 'TWUD':
				week_start = datetime.today()
				week_start -= timedelta(days=week_start.weekday())
				week_end = week_start + timedelta(days=7)
				query_set &= Q(date_posted__gte=week_start)
				query_set &= Q(date_posted__lt=week_end)

			# this month upload date
			elif search_by_date == 'TMUD':
				query_set &= Q(date_posted__month=t.month)

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
	template_name = 'recipes/user_recipes.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'recipes'
	paginate_by = 10

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
		context = super(RecipeDetailView, self).get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
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



@login_required
def RecipeCreateView(request):

	# Local variables
	categories = None
	ingredients = None

	if request.method == 'POST':
		recipe_form = RecipeForm(request.POST, request.FILES)

		if recipe_form.is_valid():
			# Get current user with their categories data from post
			recipe_form.instance.publisher = request.user
			categories = request.POST.getlist('category')
			ingredients = request.POST.getlist('ingredients')

			# Validate categories and ingredients data from post
			if len(categories) == len(ingredients) and len(categories)<10 and len(ingredients)<10:
				recipe = recipe_form.save()

				# Create categories from valid post
				for index in range(len(categories)):
					Category.objects.create(
						recipe=recipe,
						name=categories[index],
						ingredients=ingredients[index]
					)

				# Redirect user to their newly created recipe
				messages.success(request, f'Twój przepis został pomyślnie utworzony.')
				return redirect(reverse('recipe-detail', kwargs={'pk': recipe.pk}))

			else:
				# Set error message once data failed the requirements from validation
				messages.error(request, f'ERROR - Nieudana walidacja w RecipeCreateView.')
	else:
		recipe_form = RecipeForm()

	args = {}
	args['form'] = recipe_form

	# category_creation_count can be set to 0 - 9
	# It creates empty categories in the recipe-form
	if categories is None or ingredients is None:
		args['category_creation_count'] = 1
		args['categories'] = 'null'
		args['ingredients'] = 'null'
	else:
		args['category_creation_count'] = len(categories)
		args['categories'] = categories
		args['ingredients'] = ingredients

	return render(request, 'recipes/recipe_form.html', args)










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
		global recipe_id, category_query
		recipe_id = self.kwargs['pk']
		category_query = Category.objects.select_related().filter(recipe=recipe_id)
		context = super().get_context_data(**kwargs)
		context['on_update_view'] = True

		if not category_query:
			# If empty query
			# don't create empty categor(y/ies)
			context['category_creation_count'] = 0
			context['categories'] = 'null'
			context['ingredients'] = 'null'
		else:
			# If query exists, then import THIS recipe categories
			global query_ids
			categories = []
			ingredients = []
			query_ids = []

			# Extract categories(name) and ingredients from query
			for category in category_query:
				categories.append(category.name)
				ingredients.append(category.ingredients)
				query_ids.append(category.id)

			# Import categories to the template (recipe_form.html)
			context['category_creation_count'] = len(categories)
			context['categories'] = categories
			context['ingredients'] = ingredients
			
		return context




	def test_func(self):
		recipe = self.get_object()
		if self.request.user == recipe.publisher:
			return True
		return False


		

	def form_valid(self, form):

		def create_categories(category_name_list, category_ingredients_list):
			if len(category_name_list)==len(category_ingredients_list):
				for index in range(len(category_name_list)):
					# If THIS new category and ingredients is not empty
					if not (not (category_name_list[index] and not category_name_list[index].isspace())):
						if not (not (category_ingredients_list[index] and not category_ingredients_list[index].isspace())):
							# Create category
							Category.objects.create(
								recipe = Recipe.objects.get(id=recipe_id),
								name = category_name_list[index],
								ingredients = category_ingredients_list[index]
							)


		def remove_categories(old_category_id_list):
			for index in range(len(old_category_id_list)):
				Category.objects.filter(id=int(old_category_id_list[index])).delete()


		def replace_categories(mode, old_category_id_list, category_name_list, category_ingredients_list):
			# Function replace_categories is used only in [CATEGORIES VALIDATION AND IMPLEMENTATION] section
			# Also, some categories might get updated on wrong query_id, however, this is not an issue
			# because the updated query_id still belongs to THIS recipe.


			# Check if parameters are not empty.
			# Then, replace old category with new data
			def validate_and_replace(ocil, cnl, cil):
				# If THIS new category and ingredient is not empty
				if not (not (cnl and not cnl.isspace())):
					if not (not (cil and not cil.isspace())):
						# Select old category by id 
						# and replace its data with new category
						c = Category.objects.get(id=int(ocil))
						c.name = cnl
						c.ingredients = cil
						c.save()


			if mode == 'qi==nc' or mode == 'qi>nc':
				for index in range(len(category_name_list)):
					validate_and_replace(
						old_category_id_list[0],
						category_name_list[index],
						category_ingredients_list[index]
					)

					# Remove following global list element
					del query_ids[0]


			elif mode == 'qi<nc':
				for index in range(len(old_category_id_list)):
					validate_and_replace(
						old_category_id_list[index],
						category_name_list[0],
						category_ingredients_list[0]
					)

					# Remove following global list elements
					del new_categories[0]
					del new_ingredients[0]


		############################################
		# CATEGORIES VALIDATION AND IMPLEMENTATION #
		############################################

		# These global list elements are used for replace_categories function
		global new_categories, new_ingredients
		new_categories = self.request.POST.getlist('category')
		new_ingredients = self.request.POST.getlist('ingredients')


		# Before updating categories, confirm that data sent by the user is valid in terms of length and count
		if len(new_categories)==len(new_ingredients) and len(new_categories)>0 and len(new_categories)<10:


			# If there used to be no categories
			if not category_query:
				# Create new categories for THIS recipe
				create_categories(new_categories, new_ingredients)


			# If there's the same number of categories as it used to be
			elif len(query_ids)==len(new_categories):
				# Initialize old categories with new categories
				replace_categories('qi==nc', query_ids, new_categories, new_ingredients)


			# If there are less categories than it used to be
			elif len(query_ids)>len(new_categories):
				# Initialize old categories with new_categories
				replace_categories('qi>nc', query_ids, new_categories, new_ingredients)
				# Remove categories sotred in query_ids (global list element) from THIS recipe
				remove_categories(query_ids)


			# If there are more categories than it used to be
			elif len(query_ids)<len(new_categories):
				# Initialize old categories with new categories
				replace_categories('qi<nc', query_ids, new_categories, new_ingredients)
				# Create categories of new_categories + new_ingredients (global list elements) for THIS recipe
				create_categories(new_categories, new_ingredients)


			else:
				# Set error message once data failed the requirements from validation
				messages.error(self.request, f'ERROR - Nieudana walidacja w RecipeUpdateView "Niedozwolone lub brakujące porównanie".')
				return redirect(reverse('recipe-update', kwargs={'pk': recipe_id}))


		# If there are no new_categories for initialization
		elif len(new_categories)==len(new_ingredients) and len(query_ids)>0 and len(new_categories)==0:
			# Remove categories sotred in query_ids (global list element) from THIS recipe
			remove_categories(query_ids)

		######################################################
		# END OF -> CATEGORIES VALIDATION AND IMPLEMENTATION #
		######################################################


		form.instance.publisher = self.request.user
		messages.success(self.request, f'Twój przepis został pomyślnie zaktualizowany.')
		return super().form_valid(form)





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
	



def MoreInformation(request):
	return render(request, 'recipes/more_information.html')

def TermsAndConditions(request):
	return render(request, 'recipes/terms_and_conditions_pl.html')

def PrivacyAndPolicy(request):
	return render(request, 'recipes/privacy_and_policy_pl.html')

def ContactUsForm(request):
	context = {
		'BAKETOOM_MAIL_USER': os.environ.get('BAKETOOM_MAIL_USER')
	}
	return render(request, 'recipes/contact_us_form.html', context)