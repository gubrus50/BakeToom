from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
	ListView,
	DetailView,
	CreateView
)
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.contrib import messages
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



class RecipeCreateView(LoginRequiredMixin, CreateView):
	model = Recipe
	fields = ['title', 'image', 'description', 'method']



	"""
	def post(self, *args, **kwargs):
		if 'title' in self.request.POST and 'category' in self.request.POST:

			title = self.request.POST.get('title')
			categories = self.request.POST.getlist('category') 
			ingredients = self.request.POST.getlist('ingredients')
			recipe = Recipe.objects.only('id').get(title=title)

			if len(categories) == len(ingredients):
				for index in range(len(categories)):	
					Category.objects.create(
						recipe=recipe,
						title=categories[index],
						ingredients=ingredients[index]
					)

				messages.success(self.request, f'Your recipe has been successfully created')
	"""

	#return HttpResponse('ERROR')

	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, f'Your recipe has been successfully created')
		return super().form_valid(form)
