from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                error_message = "Invalid login credentials. Please try again."
        else:
            error_message = "Invalid form data. Please check the fields."
    else:
        form = LoginForm()
        error_message = None
    return render(request, 'account/login.html', {'form': form, 'error_message': error_message})