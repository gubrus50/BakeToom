from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.db.models import F
from .models import Recipe, Category

# Create your views here.

def home(request):
	context = {
		'recipes': Recipe.objects.all()
	}
	return render(request, 'recipes/home.html', context)


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


def recipe(request):

	context = {
		'recipes': Recipe.objects.all()
	}

	return render(request, 'recipes/recipe_detail.html', context)


def new_recipe(request):

	context = {
		'title': 'New recipe'
	}

	return render(request, 'recipes/new_Recipe.html', context)
