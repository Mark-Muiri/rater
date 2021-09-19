from django.shortcuts import render

# Create your views here.
class Project(models.Model):
    '''
    Class that defines the project objects
    '''
    title = models.CharField(max_length = 30)
    image = CloudinaryField('image')
    description = models.TextField()
    link = models.URLField()
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    pubdate = models.DateTimeField(auto_now_add=True, null = True)
    voters = models.ManyToManyField(User, related_name="votes")
    design_score = models.IntegerField(default=0)
    usability_score = models.IntegerField(default=0)
    content_score = models.IntegerField(default=0)
    average_design = models.FloatField(default=0,)
    average_usability = models.FloatField(default=0)
    average_content = models.FloatField(default=0)
    average_score = models.FloatField(default=0)


    def __str__(self):
        return self.title


    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    def voters_count(self):
        return self.voters.count()




    @classmethod
    def display_all_projects(cls):
        return cls.objects.all()

    @classmethod 
    def search_project(cls,name):
        return Project.objects.filter(title__icontains = name)

    @classmethod
    def get_user_projects(cls,profile):
        return cls.objects.filter(profile=profile)
