from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


@login_required
def register(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			form = UserRegisterForm(request.POST)
			if form.is_valid():
				form.save()
				username = form.cleaned_data.get('username')
				messages.success(request, f'Congratulations! Account \'{username}\' has been successfully registered.')
				return redirect('login')
		else:
			form = UserRegisterForm()
	else:
		messages.error(request, f'ERROR - You are not authorized to register.')
		return render(request, 'recipes/home.html')
	return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(
			request.POST,
			instance=request.user
		)
		p_form = ProfileUpdateForm(
			request.POST,
			request.FILES,
			instance=request.user.profile
		)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been successfully updated.')
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}


	return render(request, 'users/profile.html', context)