from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from app.models import Item 

class SignUpView(CreateView):
    model = CustomUser
    template_name = 'registration/signup.html'
    fields = [] 

    def post(self, request, *args, **kwargs):
        # 1. Extract all data including the re-added user_id
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        user_id = data.get('user_id')  # Added this back
        phone = data.get('phone_number')
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        # 2. Manual Validation logic
        if password != password_confirm:
            messages.error(request, "Passwords do not match!")
            return render(request, self.template_name)

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, self.template_name)

        if CustomUser.objects.filter(user_id=user_id).exists():
            messages.error(request, "This Student/Staff ID is already registered.")
            return render(request, self.template_name)

        # 3. Create user and login
        try:
            # Passing user_id to satisfy the database constraint
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone_number=phone,
                user_id=user_id 
            )
            login(request, user)
            messages.success(request, f"Welcome, {username}! Registration successful.")
            return redirect('item_list')
        except Exception as e:
            # This will catch things like 'IntegrityError' if ID isn't unique
            messages.error(request, f"Database Error: {e}")
            return render(request, self.template_name)

class UserLoginView(LoginView):
    template_name = 'registration/login.html'

class UserLogoutView(LogoutView):
    next_page = 'login'

@login_required
def profile_view(request):
    # This ensures the profile page shows the logged-in user's data
    my_items = Item.objects.filter(founder=request.user).order_by('-date_found')
    return render(request, 'registration/profile.html', {
        'my_items': my_items,
        'user': request.user
    })