from django.shortcuts import render,redirect
from .models import Project,Profile
from django.urls import reverse

def index(request):
    '''
    Displays landing page 
    '''
    title = "RATER"
    projects = Project.display_all_projects()
    projects_scores = Project.objects.all().order_by('-average_score')
    # highest_score = projects_scores[0]

    return render(request,"index.html",{"title": title, "projects": projects,})



def post_project(request):
    '''
    Enables a User to post a project
    '''
    if request.method == "POST":
        form = AddProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit= False)
            project.profile = request.user
            project.save()

        return redirect("index")
    else:
        form = AddProjectForm()

    return render(request, 'post_project.html', {"form": form})


def project_details(request,id):
    '''
    Show project details
    '''
    project = Project.objects.get(pk = id)
    voted = False
    if project.voters.filter(id=request.user.id).exists():
        voted = True 
    
    return render(request, 'project_details.html', {"project":project, "voted": voted})

def project_search(request):
    '''
    Display search results
    '''
    if "project" in request.GET and request.GET["project"]:
        searched_project = request.GET.get("project")
        projects = Project.search_project(searched_project)
        message =f"{searched_project}"
       
        
        return render(request, 'search.html', {"projects": projects,"message": message})
    else:
        message = "You haven't searched for any term"
        return render(request,'search.html', {"message": message}) 

def profile(request):
    '''
    Displays User's profile page
    '''
    title = 'Profile'
    current_user = request.user
    profile = Profile.objects.get(user =current_user)
    projects = Project.get_user_projects(current_user)

    return render(request, 'profile.html', {'profile':profile,"projects": projects})

def edit_profile(request):
    '''
    Edits profile
    '''
    current_user = request.user

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            bio  = form.cleaned_data['bio']
            picture = form.cleaned_data['picture']
            email  = form.cleaned_data['email']
            github_link  = form.cleaned_data['github_link']


            updated_profile = Profile.objects.get(user= current_user)
            updated_profile.bio = bio
            updated_profile.picture = picture
            updated_profile.email = email
            updated_profile.github_link  = github_link 
            updated_profile.save()
        return redirect('profile')
    else:
        form = EditProfileForm()
    return render(request, 'edit_profile.html', {"form": form})
