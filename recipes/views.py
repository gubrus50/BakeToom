from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
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
	if request.method == 'POST':
		recipe_form = RecipeForm(request.POST, request.FILES)

		if recipe_form.is_valid():
			recipe_form.instance.author = request.user
			categories = request.POST.getlist('category')
			ingredients = request.POST.getlist('ingredients')

			if len(categories) == len(ingredients) and len(categories)<10 and len(ingredients)<10:
				recipe = recipe_form.save()

				for index in range(len(categories)):
					Category.objects.create(
						recipe=recipe,
						name=categories[index],
						ingredients=ingredients[index]
					)

				messages.success(request, f'Your recipe has been successfully created')
				return redirect(reverse('recipes-home'))

			else:
				messages.error(request, f'ERROR - Failed Validation at RecipeCreateView')
				return redirect(reverse('recipes-home'))

	else:
		recipe_form = RecipeForm()

	args = {}
	args['recipe_form'] = recipe_form

	return render(request, 'recipes/recipe_form.html', args)
