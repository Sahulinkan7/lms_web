from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse

class Categories(models.Model):
    icon=models.CharField(max_length=100,null=True)
    name=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Author(models.Model):
    author_profile=models.ImageField(upload_to="Media/author")
    name=models.CharField(max_length=100,null=True)
    about_author=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
class Level(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    STATUS=(
        ('PUBLISH','PUBLISH'),
        ('DRAFT','DRAFT')
    )
    
    featured_image=models.ImageField(upload_to="Media/featured_img",null=True)
    featured_video=models.CharField(max_length=200,null=True)
    title=models.CharField(max_length=300)
    author=models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    description=models.TextField()
    level=models.ForeignKey(Level,on_delete=models.CASCADE,null=True)
    price=models.IntegerField(null=True,default=0)
    discount=models.IntegerField(null=True)
    slug=models.SlugField(default='',max_length=300,null=True,blank=True)
    status=models.CharField(choices=STATUS,max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("course_details", kwargs={"slug": self.slug})
    
    
    
def create_slug(instance,new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    qs=Course.objects.filter(slug=slug).order_by('-id')
    exists=qs.exists()
    if exists:
        new_slug="%s-%s"%(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug
    
@receiver(pre_save,sender=Course)
def pre_save_slug_creation(sender,instance,**kwargs):
    if instance.slug is None:
        instance.slug=create_slug(instance)
    
    

    
