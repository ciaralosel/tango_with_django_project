from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

@login_required
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
			return redirect(reverse('rango:index'))
		else:
			#Supplied form contained errors so print them to terminal
			print(form.errors)

	#Will handle bad form, new form or no form.
	#Render form with error messages if any
	return render(request, 'rango/add_category.html', {'form': form})
	
@login_required
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	#Can't add page to category that doesn't exist
	if category is None:
		return redirect(reverse('rango:index'))

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

def register(request):
	#Boolean for telling template whether the registration was succesful
	#False initially and changes when registration succeeds.
	registered = False

	#If HTTP POST we want to process form data
	if request.method == 'POST':
		#Try to grab info from form info
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		#If two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			#Save user's form data to database
			user = user_form.save()
			
			#Now hash password with set_password method
			#Once hashed we can update user object
			user.set_password(user.password)
			user.save()

			#Now sort out UserProfile instance
			#Since we need to set user attribute ourselves, set commit=False which delays saving model until ready to avoid integrity problems
			profile = profile_form.save(commit=False)
			profile.user = user

			#Did user provide profile pic? If so need to get from input form and put in UserProfile model
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			#Now save UserProfile model instance
			profile.save()

			#Update variable to indicate template registration was succesful
			registered = True
		else:
			#Invalid form so print problems to terminal
			print(user_form.errors, profile_form.errors)
	else:
		#Not HTTP POST so render form using two ModelForm instances 
		#These forms will be blank ready for user input
		user_form = UserForm()
		profile_form = UserProfileForm()

	#Render template depending on context
	return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
	#If HTTP POST request try to pull out relevant info:
	if request.method == 'POST':
		#Gather username & password provided, obtained via login form.
		#Use request.POST.get('<variable>') instead of request.POST['variable'] as it returns None if value doesn't exist while other raises exception
		username = request.POST.get('username')
		password = request.POST.get('password')

		#See if combination is valid
		user = authenticate(username=username, password=password)

		#If we get User object = details correct
		#If None = no use with matching credentials
		if user:
			#Is account active?
			if user.is_active:
				#Can log user in and send back to homepage
				login(request, user)
				return redirect(reverse('rango:index'))
			else:
				#Inactive account
				return HttpResponse("Your Rango account is disabled.")
		else:
			#Bad login details
			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("Invalid login details supplied.")
	
	#Not HTTP POST so display login form
	#Most likely HTTP GET
	else:
		#No context variables to pass
		return render(request, 'rango/login.html')

@login_required
def restricted(request):
	return render(request, 'rango/restricted.html')

#Use login_required() decorator to ensure only logged in users can access views
@login_required
def user_logout(request):
	#Since we know user is logged in we can now log them out
	logout(request)
	#Take user back to homepage
	return redirect(reverse('rango:index'))