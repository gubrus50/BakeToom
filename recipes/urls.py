from django.urls import path
from .views import RecipeListView, RecipeDetailView, RecipeCreateView
from . import views

urlpatterns = [
	path('', RecipeListView.as_view(), name='recipes-home'),
	path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
	path('recipe/new/', RecipeCreateView, name='recipe-create'),
]