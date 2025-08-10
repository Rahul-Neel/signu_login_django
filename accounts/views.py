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


# accounts/views.py (append)

from .models import Category, BlogPost
from django.contrib import messages
from django.shortcuts import get_object_or_404

def create_post_view(request):
    # Only doctors can create posts
    if not request.user.is_authenticated or request.user.user_type != 'doctor':
        return redirect('login')

    categories = Category.objects.all()
    error = None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category_id = request.POST.get('category')
        summary = request.POST.get('summary', '').strip()
        content = request.POST.get('content', '').strip()
        is_draft = True if request.POST.get('is_draft') == 'on' else False
        image = request.FILES.get('image')

        if not title or not summary or not content or not category_id:
            error = "Please fill title, category, summary and content."
        else:
            category = get_object_or_404(Category, id=category_id)
            post = BlogPost.objects.create(
                author=request.user,
                title=title,
                category=category,
                summary=summary,
                content=content,
                is_draft=is_draft,
                image=image
            )
            messages.success(request, "Post created successfully.")
            return redirect('doctor_posts')

    return render(request, 'create_post.html', {'categories': categories, 'error': error})

@login_required
def doctor_posts(request):
    if request.user.user_type != 'doctor':
        return redirect('login')
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'doctor_posts.html', {'posts': posts})

# views.py
def categories_list(request):
    categories = Category.objects.all()
    for c in categories:
        c.published_count = c.posts.filter(is_draft=False).count()
    return render(request, "categories.html", {"categories": categories})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # show only non-draft posts
    posts = category.posts.filter(is_draft=False).order_by('-created_at')
    return render(request, 'category_posts.html', {'category': category, 'posts': posts})

