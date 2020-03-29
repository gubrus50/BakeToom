from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import F
from .models import Recipe, Category
from .forms import RecipeForm, CategoryForm



class RecipeListView(ListView):
	model = Recipe
	template_name = 'recipes/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'recipes'
	ordering = [F('title').asc(nulls_last=True)] # ORDER BY title & If title=null, null go last.



class RecipeDetailView(DetailView):
	model = Recipe
	def get_context_data(self, **kwargs):
		context = super(RecipeDetailView, self).get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
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
				messages.success(request, f'Your recipe has been successfully created')
				return redirect(reverse('recipe-detail', kwargs={'pk': recipe.pk}))

			else:
				# Set error message once data failed the requirements from validation
				messages.error(request, f'ERROR - Failed Validation at RecipeCreateView')
	else:
		recipe_form = RecipeForm()

	args = {}
	args['recipe_form'] = recipe_form

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

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
