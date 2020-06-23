from django.urls import path
from .views import (
	AboutView,
	ContactUsForm,
	PrivacyAndPolicy,
	RecipeListView,
	RecipeDetailView,
	RecipeCreateView,
	RecipeUpdateView,
	RecipeDeleteView,
	RecipePlainView,
	TermsAndConditions,
	UserRecipeListView
)
from . import views

urlpatterns = [
	path('', RecipeListView.as_view(), name='recipes-home'),
	path('user/<str:username>/', UserRecipeListView.as_view(), name='user-recipes'),
	path('recipe/new/', RecipeCreateView.as_view(), name='recipe-create'),
	path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
	path('recipe/plain/<int:pk>/', RecipePlainView.as_view(), name='recipe-plain'),
	path('recipe/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),
	path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
	path('about/', AboutView, name='about'),
	path('about/contact-us-form', ContactUsForm, name='contact-us-form'),
	path('about/privacy-and-policy/', PrivacyAndPolicy, name='privacy-and-policy'),
	path('about/terms-and-conditions/', TermsAndConditions, name='terms-and-conditions')
]