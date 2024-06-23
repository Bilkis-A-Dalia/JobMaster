from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.db.models import Sum
from decimal import Decimal

# from django.utils.text import force_text
from . import forms
from django.views import View
from django.shortcuts import render, redirect
from .forms import ResumeForm,ReviewForm
from .models import Resume

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f'https://jobmaster-8u2u.onrender.com/user/active/{uid}/{token}/'
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
        return redirect('user_login')
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
    return redirect('home')

# profile update  
class UserAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form =forms.UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


def create_or_edit_resume(request):
    # Check if the user already has a resume
    try:
        resume = request.user.resume
        editing = True
    except Resume.DoesNotExist:
        resume = None
        editing = False
    
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('profile')
    else:
        form = ResumeForm(instance=resume)
    
    return render(request, 'profile.html', {'form': form, 'editing': editing})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        profile_form = forms.UserUpdateForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': profile_form})

# services
def services(request):
    return render(request, 'services.html')

# about
def about(request):
    return render(request, 'about.html')

# contact_us
def contactUs(request):
    return render(request, 'contact_form.html')


# passchange
def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html', {'form' : form})


# Reset password mail
def reset_password(request):
    if request.method == 'POST':
        form = forms.PasswordResetForm(request.POST)
        if form.is_valid():
            # Get users by email
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                # Choose one user (for example, the first one)
                user = users.first()

                # Generate a password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Build the password reset link
                reset_link = request.build_absolute_uri(f"https://jobmaster-8u2u.onrender.com/user/passchange/{uid}/{token}")

                # Send the password reset link to the user's email
                email_subject = "Password Reset Request"
                email_body = render_to_string('password_reset_email.html', {'reset_link': reset_link})
                email = EmailMultiAlternatives(email_subject, '', to=[email])
                email.attach_alternative(email_body, 'text/html')
                email.send()

                messages.success(request, 'Password reset link has been sent to your email.')
                return redirect('user_login')
            else:
                messages.error(request, 'Email does not exist.')
    else:
        form = forms.PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})

def pass_change2(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form=SetPasswordForm(user=user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user)
                return redirect('user_login')
        else:
            form=SetPasswordForm(user=user)
        return render(request, 'passchange.html', {'form':form})
    else:
        return redirect('user_login')

