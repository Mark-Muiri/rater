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
