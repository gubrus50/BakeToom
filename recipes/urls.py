from django.urls import path
from .views import RecipeListView, RecipeDetailView
from . import views

urlpatterns = [
	path('', RecipeListView.as_view(), name='recipes-home'),
	path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
	path('recipe/', views.recipe, name='recipe'),
	path('recipe/new/', views.new_recipe, name='new_recipe')
]