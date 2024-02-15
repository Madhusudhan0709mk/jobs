from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .forms import ProfileForm,createjobpostsForm,contactForm
from .models import Profile,createjobposts,applyjob
from django.core.paginator import Paginator
from django.views import View
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv
from django.http import HttpResponse
from django.db.models import Q
def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def listjobs(request):
    posts = createjobposts.objects.all()
    #setup pagination
    p = Paginator(createjobposts.objects.all(),3)
    page = request.GET.get('page')
    pos = p.get_page(page)
    return render(request,'listjobs.html',{'posts':posts,'pos':pos})

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
    user_applied_jobs = applyjob.objects.filter(user=request.user)
    profiles = Profile.objects.all()
    return render(request,'listprofiles.html',{'profiles':profiles,'user_applied_jobs':user_applied_jobs})

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
    
def viewjobdetailsdelete(request,pk):
    if request.user.is_authenticated:
        delete_it = createjobposts.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,'you have deleted the job post')
        return redirect('index')
    else:
        messages.info(request,'You must be logged in to use the page')
        return redirect('index')
    
def viewjobdetailsupdate(request,pk):
    if request.user.is_authenticated:
        viewjobs= createjobposts.objects.get(id=pk)
        form = createjobpostsForm(request.POST or None, instance=viewjobs)
        if form.is_valid():
            form.save()
            messages.success(request, "post Has Been Updated!")
            return redirect('viewjobdetails', pk=viewjobs.id)
        return render(request,'viewjobdetailsupdate.html',{'form':form})
    else:
        messages.info(request,'You must be logged in to use the page')
        return redirect('index')
    
def applytojob(request,pk):
    job = createjobposts.objects.get(pk=pk)
    applyjob.objects.create(
        createjobposts = job,
        status = 'pending',
        user=request.user
    )
    messages.success(request,'You have applied job successfully')
    return redirect('index') 

def applicants(request,pk):
    job = get_object_or_404(createjobposts, pk=pk)

    applicants = job.applyjob_set.filter(status__in=['pending', 'accepted', 'declined'])
    context = {
        'job': job,
        'applicants': applicants,

    }
    return render(request,'applicants.html',context)

class DownloadApplicantsCSVView(View):
    def get(self, request, pk):
        job = get_object_or_404(createjobposts, pk=pk)
        applicants = job.applyjob_set.filter(status__in=['pending', 'accepted', 'declined'])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="applicants_{job.companyname}.csv"'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Name', 'Email', 'Bio', 'Phone', 'Address', 'City', 'Zipcode', 'Created_at'])

        for applicant in applicants:
            csv_writer.writerow([
                applicant.user.username,
                applicant.user.email,
               
            ])

        return response
    
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = createjobposts.objects.filter(Q(companyname__icontains=searched)|Q(address__icontains=searched))
        return render(request,"listjobs.html",{'searched':searched})
        # if not searched:
        #     messages.success(request,'NO RESULTS FOUND ')
        #     return render(request,"listjobs.html")
        # else:
        #     return render(request,"listjobs.html")   
    else:
        messages.success(request,'NO RESULTS FOUND ')
        return render (request,'listjobs.html')
    
def contact(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = contactForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Your message is submmitted')
                return redirect('index')
        else:
            return render(request,'contact.html')
    else:
        return render(request,'contact.html')