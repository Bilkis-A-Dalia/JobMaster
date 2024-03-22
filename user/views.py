from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.db.models import Sum
from decimal import Decimal
# from django.utils.text import force_text
from . import forms
from django.views import View

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f'http://127.0.0.1:8000/user/active/{uid}/{token}/'
            email_subject = 'Confirm Your Email'
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})

            try:
                # send email
                email = EmailMultiAlternatives(email_subject, '', to=[user.email])
                email.attach_alternative(email_body, "text/html")
                email.send()
                messages.success(request, 'Account verification mail sent successfully')
                return redirect('register')
            except Exception as e:
                messages.error(request, f'Error sending verification email: {e}')
    else:
        register_form = forms.RegistrationForm()

    return render(request, 'register.html', {'form': register_form, 'type': 'Register'})


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account successfully activated. You can now log in.')
        return redirect('register')
    else:
        messages.error(request, 'Invalid activation link. Please try again or contact support.')
        return redirect('register')
    

# login 
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_pass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('home')
        messages.warning(request, 'Login information incorrect')
        return render(request, 'login.html', {'form': form, 'type': 'Login'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'type': 'Login'})

def user_logout(request):
    logout(request)
    return redirect('user_login')

    
class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form =forms.UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
