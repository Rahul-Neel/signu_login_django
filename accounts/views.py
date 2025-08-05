from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.core.files.storage import FileSystemStorage

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    user_type = request.GET.get('type', 'patient')
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type_form = request.POST['user_type']

        user = authenticate(username=username, password=password)
        if user and user.user_type == user_type_form:
            login(request, user)
            if user.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
        else:
            error = "Invalid credentials or wrong user type."

    return render(request, 'login.html', {'user_type': user_type, 'error': error})

def signup_view(request):
    user_type = request.GET.get('type', 'patient')
    error = None
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        address_line1 = request.POST['address_line1']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        profile_picture = request.FILES.get('profile_picture')

        if password != confirm_password:
            error = "Passwords do not match!"
        elif CustomUser.objects.filter(username=username).exists():
            error = "Username already taken!"
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                address_line1=address_line1,
                city=city,
                state=state,
                pincode=pincode,
                profile_picture=profile_picture
            )
            return redirect(f'/login/?type={user_type}')

    return render(request, 'signup.html', {'user_type': user_type, 'error': error})

@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html', {'user': request.user})

@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')
