from django.urls import path
from .views import (
	MoreInformation,
	PrivacyAndPolicy,
	RecipeListView,
	RecipeDetailView,
	RecipeCreateView,
	RecipeUpdateView,
	RecipeDeleteView,
	TermsAndConditions,
	UserRecipeListView
)
from . import views

urlpatterns = [
	path('', RecipeListView.as_view(), name='recipes-home'),
	path('user/<str:username>/', UserRecipeListView.as_view(), name='user-recipes'),
	path('recipe/new/', RecipeCreateView, name='recipe-create'),
	path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
	path('recipe/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),
	path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
	path('more/information', MoreInformation, name='more-information'),
	path('more/privacy-and-policy/', PrivacyAndPolicy, name='privacy-and-policy'),
	path('more/terms-and-conditions/', TermsAndConditions, name='terms-and-conditions')
]