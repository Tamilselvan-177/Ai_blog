from django.shortcuts import render, redirect
from .generator import main  # Assuming 'main' function is properly defined in generator.py
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import GeneratedText
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404

# URL generation view
def genai(request):
    if request.method == "POST":
        url = request.POST.get('url')  # Using POST to get the URL

        # Assuming 'main' function processes the URL and returns a tuple (title, text)
        text = main(url)

        # Check if the 'text' is in the correct format (tuple with two elements)
        try:
                # Ensure the user is authenticated
                if request.user.is_authenticated:
                    user = User.objects.get(username=request.user.username)

                    # Create a GeneratedText instance
                    generated_text = GeneratedText(
                        user=user,
                        url=url,
                        text=text[1],
                        title=text[0]
                    )

                    # Save the object to the database
                    generated_text.save()
                    return render(request, "index.html", {"text": text[1]})  # Pass 'text' to template

                else:
                    messages.error(request, "You need to log in to generate text.")
                    return redirect('login')  # Redirect to login if not authenticated
        except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('login')  # Redirect to login page if user doesn't exist
        else:
            messages.error(request, "Invalid response from the generator.")
            return redirect('genai')  # Redirect to the generation page if invalid response
    return render(request, "index.html")  # Render empty template if no POST request

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('genai')  # Redirect to home after login
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('genai')  # Redirect to home after logout

# Signup view
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('genai')  # Redirect to home after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# View to display a single blog's details

def blog_list(request):
    # Get the logged-in user
    if request.user.is_authenticated:
        user = request.user

        # Filter the blog posts by the current user's username
        blogs = GeneratedText.objects.filter(user=user)

        return render(request, 'blogs.html', {'blogs': blogs})
    return redirect('login')  # Redirect to login if not authenticated
@login_required
def blog_detail(request, id):
    # Retrieve the blog post by id or return 404 if not found
    blog = get_object_or_404(GeneratedText, id=id)
    return render(request, 'openblog.html', {'blog': blog})