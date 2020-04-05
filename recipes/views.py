from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin
)
from django.contrib.auth.decorators import login_required
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	DeleteView
)
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import F
from .models import Recipe, Category
from .forms import RecipeForm, CategoryForm




class RecipeListView(ListView):
	model = Recipe
	template_name = 'recipes/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'recipes'
	paginate_by = 5

	def get_queryset(self):
		query = self.request.GET.get('title')
		if query:
			object_list = self.model.objects.filter(title__icontains=query).order_by('title')
		else:
			object_list = self.model.objects.all().order_by('title')
		return object_list




class UserRecipeListView(ListView):
	model = Recipe
	template_name = 'recipes/user_recipes.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'recipes'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		query = self.request.GET.get('title')
		
		if query:
			object_list = self.model.objects.filter(author=user, title__icontains=query).order_by('title')
		else:
			object_list = self.model.objects.filter(author=user).order_by('title')
		return object_list





class RecipeDetailView(DetailView):
	model = Recipe
	def get_context_data(self, **kwargs):
		context = super(RecipeDetailView, self).get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['authenticated_user'] = self.request.user
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
			recipe_form.instance.author = request.user
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
	fields = ['title', 'image', 'description', 'method']


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
		if self.request.user == recipe.author:
			return True
		return False


		

	def form_valid(self, form):

		def create_categories(category_name_list, category_ingredients_list):
			if len(category_name_list)==len(category_ingredients_list):
				for index in range(len(category_name_list)):
					# If THIS new category and ingredient is not empty
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


		def replace_categories(loop, remove_global_list, old_category_id_list, category_name_list, category_ingredients_list):
			# In this method new_categories might get updated on wrong category (from this recipe of corse),
			# however, in this case it dosen't matter because the following
			# categories are linked with THIS recipe id.

			def validate_and_create(ocil, cnl, cil):
				# If THIS new category and ingredient is not empty
				if not (not (cnl[index] and not cnl[index].isspace())):
					if not (not (cil[index] and not cil[index].isspace())):
						# Select old category by id 
						# and replace its data with new category
						c = Category.objects.get(id=int(ocil[index]))
						c.name = cnl[index]
						c.ingredients = cil[index]
						c.save()

			if loop == "by_new":
				for index in range(len(category_name_list)):
					validate_and_create(old_category_id_list, category_name_list, category_ingredients_list)
					if remove_global_list==True:
						# GLOBAL LIST
						del query_ids[index]

			elif loop == "by_old":
				for index in range(len(old_category_id_list)):
					validate_and_create(old_category_id_list, category_name_list, category_ingredients_list)
					if remove_global_list==True:
						# GLOBAL LIST
						del new_categories[index]
						del new_ingredients[index]


		############################################
		# CATEGORIES VALIDATION AND IMPLEMENTATION #
		############################################

		global new_categories, new_ingredients
		new_categories = self.request.POST.getlist('category')
		new_ingredients = self.request.POST.getlist('ingredients')

		# If submitted categories names are same length as submitted categories ingredients,
		# ff so, are their elements count between 1 and 9
		if len(new_categories)==len(new_ingredients) and len(new_categories)>0 and len(new_categories)<10:

			# If there are no categories in THIS recipe
			if not category_query:
				# Create new categories for THIS recipe
				create_categories(new_categories, new_ingredients)

			# If old categories length is same as new categories length
			elif len(query_ids)==len(new_categories):
				# Initialize old categories with new_categories
				# and don't remove global list elements
				replace_categories("by_new", False, query_ids, new_categories, new_ingredients)

			# If there were more categories in THIS recipe than submitted
			elif len(query_ids)>len(new_categories):
				# Initialize old categories with new_categories
				# and remove global list elements
				replace_categories("by_new", True, query_ids, new_categories, new_ingredients)
				# Remove leftover, old categories
				remove_categories(query_ids)

			# If there is not enough old categories to initialize new categories
			elif len(query_ids)<len(new_categories):
				# Initialize old categories with new_categories
				# and remove global list elements
				replace_categories("by_old", True, query_ids, new_categories, new_ingredients)
				# Create the leftover new categories for THIS recipe
				create_categories(new_categories, new_ingredients)

			else:
				# Set error message once data failed the requirements from validation
				messages.error(self.request, f'ERROR - Nieudana walidacja w RecipeUpdateView "Niedozwolone lub brakujące porównanie".')
				return redirect(reverse('recipe-update', kwargs={'pk': recipe_id}))


		# If there are no new_categories for initialization
		elif len(new_categories)==len(new_ingredients) and len(query_ids)>0 and len(new_categories)==0:
			# Remove leftover, old categories 
			remove_categories(query_ids)

		######################################################
		# END OF -> CATEGORIES VALIDATION AND IMPLEMENTATION #
		######################################################

		form.instance.author = self.request.user
		messages.success(self.request, f'Twój przepis został pomyślnie zaktualizowany.')
		return super().form_valid(form)








class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Recipe
	success_url = '/'
	success_message = 'Your recipe has been successfully removed.'

	def test_func(self):
		recipe = self.get_object()
		if self.request.user == recipe.author:
			return True
		return False

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(RecipeDeleteView, self).delete(request, *args, **kwargs)
	