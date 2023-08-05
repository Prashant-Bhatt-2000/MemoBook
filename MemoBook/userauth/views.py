from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from .models import User, Memo
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password, check_password

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not name or not email or not password: 
            messages.error(request, 'Please fill the form properly')
        else: 
            user_exists = User.objects.filter(email=email).exists()

            if user_exists:
                messages.error(request, 'User already exists')
            else:

                passwordhash = make_password(password)
                # Create and save the user with a hashed password
                user = User(name= name, email=email, password = passwordhash)
                user.save()
                messages.success(request, 'User successfully registered')
                return redirect('login')  # Redirect to the login page after successful registration

    return render(request, 'register.html')



def loginuser(request): 
    if request.method == "POST":
        email = request.POST.get('loginemail')
        password = request.POST.get('loginpassword')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.success(request, 'User Not Found')

        if user is not None:
            password_correct = check_password(password, user.password)
            print(f'password_correct: {password_correct}')
            if password_correct:
                if user:
                    login(request, user)
                    messages.success(request, 'Logged in successfully')
                    return redirect('home')
                else:
                    messages.error(request, 'Authentication failed')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'User with the provided email does not exist.')

    return render(request, 'login.html')



@login_required
def home(request):
    if request.method == "POST": 
        memo_text = request.POST.get('memo')

        if not memo_text:
            messages.info(request, 'Please add a task first')
        else: 
            current_user = request.user

            memo_item = Memo(author=current_user, memo=memo_text)
            memo_item.save()

            messages.success(request, 'Task Added')

    return render(request, 'home.html')



@login_required
def tasks(request):
    if request.method == "GET": 
        current_user = request.user
        memo = Memo.objects.filter(author=current_user)
        print(memo)
        return render(request, 'notes.html', {'memo': memo})
    return render(request, 'notes.html')


@login_required
def delete_memo(request, memo_id):
    if request.method == "GET":
        memo = Memo.objects.get(id=memo_id, author=request.user)
        memo.delete()
        messages.success(request, 'Memo Completed successfully')

        return redirect('notes')
    
    return redirect('notes')


def edit_memo(request, memo_id):

    return redirect('notes')