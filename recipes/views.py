from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):

	class Recipe:
		def __init__(self,title,description,image):
			self.title=title
			self.description=description
			self.image=image

	description = "This is a breath description about the following recipe. It is very useful when you are not sure if the recipe will be the one you're looking for. This helpul message will guide you in the search of your desires."
	url = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fnutritiouslife.com%2Fwp-content%2Fuploads%2F2012%2F03%2Fhomemade-chicken-soup.jpg&f=1&nofb=1"

	context = {
		'title': 'Home',
		'recipes': [
			Recipe('Pomidorowa',description,"https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.smakipodbeskidzia.pl%2Fpliki%2Fprzepisy%2F137881895213871400.jpg&f=1&nofb=1"),
			Recipe('Grzybowa',description,"https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F1.bp.blogspot.com%2F-GaIVuv812O0%2FWIkToLWNNbI%2FAAAAAAAAYQs%2FYbKDQlr_FKw6FBRM0jmSpAz0adjuWv7YwCLcB%2Fs1600%2F_1120989.JPG&f=1&nofb=1"),
			Recipe('Barszcz Biały',description,"https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwysmienity.pl%2Fwp-content%2Fuploads%2F2016%2F03%2Fbarszczbialy.jpg&f=1&nofb=1"),
			Recipe('Barszcz Czerwony',description,"https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2FaQQRXiYSMmo%2Fmaxresdefault.jpg&f=1&nofb=1"),
			Recipe('Schabowe',description,"https://d3iamf8ydd24h9.cloudfront.net/pictures/articles/2019/05/583005-v-1000x1000.jpg")
		]
	}

	return render(request, 'recipes/home.html', context)



def recipe(request):

	context = {
		'title': 'Recipe'
	}

	return render(request, 'recipes/recipe.html', context)


def new_recipe(request):

	context = {
		'title': 'New recipe'
	}

	return render(request, 'recipes/new_Recipe.html', context)
