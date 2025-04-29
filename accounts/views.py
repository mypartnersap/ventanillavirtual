# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField
from django.urls import reverse_lazy
from django.views import generic
# Customize accounts
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# Custom Form
from accounts.forms import CustomPasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
# SignUp
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .models import Profile
from record_management.views import index


class ResetView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('reset')
    template_name = 'registration/reset.html'


class MyPasswordResetView(PasswordResetView):
	form_class = CustomPasswordResetForm
	def form_valid(self, form):
		username = form.cleaned_data.get('username')
		email = form.cleaned_data.get('email', '').lower()
		try:
			user = get_user_model().objects.get(username=username, email=email)
		except(get_user_model().DoesNotExist):
			user = None
		if user is None:
			return redirect('password_reset_done')
		return super().form_valid(form)


def register(request): # Vista para el registro de usuarios
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Profile
            companyid = form.cleaned_data.get('companyid')
            numberId = form.cleaned_data.get('numberId')
            taxNumberType = form.cleaned_data.get('taxNumberType')

            Profile.objects.create(user=user, companyid=companyid, numberId=numberId, taxNumberType=taxNumberType)
            # Login
            login(request, user)
            return redirect(index)
    else:
        form = UserRegistrationForm()
        return render(request, 'registration/signup.html', {'form': form})
    return render(request, 'registration/signup.html', {'form': form})
