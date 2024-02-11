from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .forms import ProfileForm,createjobpostsForm
from .models import Profile,createjobposts
def index(request):
    posts = createjobposts.objects.all()
    return render(request,'index.html',{'posts':posts})
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
               messages.info(request,'username taken already')
               return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')   
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                messages.info(request,'user created') 
                return redirect('login')
        else:
            messages.info(request,'password not matching')
        return redirect('register')
    else:
        return render(request,'register.html')
    
# the login logic
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
    # logout
def logout(request):
    auth.logout(request)
    return redirect('/')

def about(request):
    return render(request,'about.html')


def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'profile_view.html', {'profile': profile})

def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=user.profile)

    return render(request, 'profile_edit.html', {'form': form})

def listprofiles(request):
    profiles = Profile.objects.all()
    return render(request,'listprofiles.html',{'profiles':profiles})

def create_job_posts(request):
    if request.user.is_authenticated and request.user.username =="recruiter":
        if request.method == 'POST':
            form = createjobpostsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
            messages.success(request,'Your form is submitted')
        else:
            form = createjobpostsForm()
        return render(request,'createjobposts.html',{'form':form})
    else:
        return render(request,'createjobposts.html')
    
def viewjobdetails(request,pk):
    if request.user.is_authenticated:
        viewjobs= get_object_or_404(createjobposts, id=pk)
        return render(request,'viewjobdetails.html',{'viewjobs':viewjobs})
    else:
        messages.info(request,'You must be logged in to use the page')
        return redirect('index')