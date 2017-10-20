from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')


def linkedin(request):
    return redirect('https://www.linkedin.com/in/matthew-osborne-33b89b9b/')

