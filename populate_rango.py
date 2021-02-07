import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
		      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
	#First we create lists of dictionaries containing pages we want to add to each category
	#Then we create dictionary of dicts for categories which allows us to iterate through each structure

	python_pages = [
		{'title': 'Official Python Tutorial',
		 'url':'http://docs.python.org/3/tutorial/', 'views':1},
		{'title': 'How to Think Like a Computer Scientist',
		 'url':'http://www.greenteapress.com/3/thinkpython/', 'views':2},
		{'title': 'Learn Python in 10 Minutes',
		 'url':'http://www.korokithakis.net/tutorials/python/', 'views':3} ]

	django_pages = [
		{'title': 'Official Django Tutorial',
		 'url':'http://docs.djangoproject.com/en/2.1/intro/tutorial01/', 'views':4},
		{'title': 'Django Rocks',
		 'url':'http://www.djangorocks.com/', 'views':5},
		{'title': 'How to Tango with Django',
		 'url':'http://www.tangowithdjango.com/', 'views':6} ]

	other_pages = [
		{'title': 'Bottle',
		 'url':'http://bottlepy.org/docs/dev/', 'views':7},
		{'title': 'Flask',
		 'url':'http://flask.pocoo.org', 'views':8} ]

	cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
		'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
		'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16} }

	#If you want to add more add to dictionaries above

	#Code below goes through cats dict, adds each category and adds them to associated pages
	for cat, cat_data in cats.items():
		c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
		for p in cat_data['pages']:
			add_page(c, p['title'], p['url'], views=p['views'])

	#Print out categories added
	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
	p = Page.objects.get_or_create(category=cat, title=title)[0]
	p.url=url
	p.views=views
	p.save()
	return p

def add_cat(name, views=0, likes=0):
	c = Category.objects.get_or_create(name=name)[0]
	c.views=views
	c.likes=likes
	c.save()
	return c

#Start execution here
if __name__ == '__main__':
	print('Starting Rango population script...')
	populate()


		