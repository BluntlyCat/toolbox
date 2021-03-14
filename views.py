from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth.decorators import login_required
from toolbox.forms import LoginForm
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user and user.is_active:
                django_login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)

            raise PermissionError

    return render(request, 'toolbox/login.html', {
        'form': LoginForm(),
        'login_url': 'login',
    })


@login_required
def user_logout(request):
    django_logout(request)
    return redirect('login')
