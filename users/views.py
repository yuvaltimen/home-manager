from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegisterForm


def register(req):
    if req.method == "POST":
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(req, f"Account created for user: {username}")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(req, 'users/register.html', {'form': form})


def logout_view(req):
    logout(req)
    return render(req, 'users/logout.html')


@login_required
def profile(req):
    return render(req, 'users/profile.html')


