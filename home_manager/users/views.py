from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


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
    if req.method == "POST":
        user_update_form = UserUpdateForm(req.POST, instance=req.user)
        profile_update_form = ProfileUpdateForm(req.POST,
                                                req.FILES,
                                                instance=req.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(req, "Account updated successfully!")
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=req.user)
        profile_update_form = ProfileUpdateForm(instance=req.user.profile)

    ctx = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }
    return render(req, 'users/profile.html', ctx)


