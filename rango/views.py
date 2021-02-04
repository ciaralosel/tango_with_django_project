from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #Construct dictionary to pass to template engine as its context.
    #Key boldmessage matched to {{ boldmessage }} in template.
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    #Return rendered response to send to client.
    #Make use of shortcut function.
    #First parameter is template we want to use.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    #return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")
    return render(request, 'rango/about.html')

