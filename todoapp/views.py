from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request , 'home.html',{'todos':todos})



def signupuser(request):
    if request.method == 'GET':
        return render(request , 'signupuser.html',{'form':UserCreationForm()})
    else:
        #Create A New User
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('create')
        except IntegrityError:
            return render(request , 'signupuser.html',{'form':UserCreationForm(),'usernameerror':'Username already exsists'})
        else:
            return render(request , 'signupuser.html',{'form':UserCreationForm(),'passworderror':'Password didn\'t match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request , 'loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'] )
        if user is  None:
            return render(request , 'loginuser.html',{'form':AuthenticationForm(),'error':'Username or Password didn\'t match'})

        else:
            login(request,user)
            return redirect('home')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')

@login_required
def create(request):
    if request.method == 'GET':
        return render(request , 'create.html',{'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('home')
        except ValueError:
            return render(request , 'create.html',{'form':TodoForm(),'error':'Bad Data Passing'})
@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == 'GET':
        form = TodoForm(instance = todo)
        return render(request,'viewtodo.html',{'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance = todo)
            form.save()
            return redirect('home')

        except ValueError:
            return render(request , 'viewtodo.html',{'todo':todo,'error':'Bad Data Passing'})

@login_required
def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('home')
@login_required
def completed(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'completed.html',{'todos':todos})
@login_required
def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('home')
