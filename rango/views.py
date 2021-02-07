from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import PageForm

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

def add_category(request):
	form = CategoryForm()
	
	#A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		#Have we been provided with valid form?
		if form.is_valid():
			#Save new category to database
			form.save(commit=True)
			#Now category is saved we could confirm this, but for now just redirect user back to index view
			return redirect('/rango/')
		else:
			#Supplied form contained errors so print them to terminal
			print(form.errors)

	#Will handle bad form, new form or no form.
	#Render form with error messages if any
	return render(request, 'rango/add_category.html', {'form': form})
	
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	#Can't add page to category that doesn't exist
	if category is None:
		return redirect('/rango/')

	form = PageForm()
	
	if request.method == 'POST':
		form = PageForm(request.POST)

		#Have we been provided with valid form?
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
		else:
			#Supplied form contained errors so print them to terminal
			print(form.errors)

	context_dict = {'form': form, 'category': category}
	#Will handle bad form, new form or no form.
	#Render form with error messages if any
	return render(request, 'rango/add_page.html', context=context_dict)

