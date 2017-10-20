from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
# Create your views here.


def index(request):
    context = {}
    return render(request, 'userauth/index.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
    else:
        form=UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'userauth/register.html', context)






