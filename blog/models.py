
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver


# name of the file where image is stored
def upload_location(instance, filename):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id),
        title = str(instance.title),
        filename = filename
    )
    return file_path


class BlogPost(models.Model):
	title 					= models.CharField(max_length=50, null=False, blank=False)
	body 					= models.TextField(max_length=5000, null=False, blank=False)
	image		 			= models.ImageField(upload_to=upload_location, null=True, blank=True)
	date_published 			= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated 			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug 					= models.SlugField(blank=True, unique=True)

	def __str__(self):
		return self.title

@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    # delete images if blog post is deleted
    instance.image.delete(False)

# called before blog post is actually commited    
def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    # intercepts requests // intercepts the saving of the post and executes action before it is saved
    if not instance.slug:
        instance.slug = slugify(instance.author.username+'-'+instance.title)

# connecting our presave function to the presave // if blogpost attempted to be saved in the database, do this fx and then commit
pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
