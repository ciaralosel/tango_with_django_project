from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

def index(request):
	#Query database for list of all categories currently stored ordered by descending number of likes
	#Retrieve top 5
	#Place list in context_dict
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	
	context_dict = {}
	context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
	context_dict['categories'] = category_list
	context_dict['pages'] = page_list

	#Return rendered response to send to client.
	#Make use of shortcut function.
	#First parameter is template we want to use.
	return render(request, 'rango/index.html', context=context_dict)

def about(request):
    #return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
	#Create context dict which we pass to template rendering engine
	context_dict = {}
	
	try:
		#Can we find category name slug with given name?
		#If not, .get() raises DoesNotExist or, if yes, returns one model instance
		category = Category.objects.get(slug=category_name_slug)

		#Retrieve associated pages. filter() returns list of page objects or empty list
		pages = Page.objects.filter(category=category)

		#Adds results list to template context under name pages
		context_dict['pages'] = pages
		#We also add category object from database to context dictionary - use this to verify category exists.
		context_dict['category'] = category
	except:
		#Get here if we didn't find category.
		#Template will display 'no category' message for us.
		context_dict['category'] = None
		context_dict['pages'] = None

	#Render response and return to client
	return render(request, 'rango/category.html', context=context_dict)

