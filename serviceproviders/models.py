from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from PIL import Image  # Import the Image class from Pillow
from moviepy.editor import VideoFileClip

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)

class Service(models.Model):
    service_name = models.CharField(max_length=100)
    service_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    service_video = models.FileField(upload_to='service_videos/', null=True, blank=True)
    service_picture = models.FileField(upload_to='service_pictures/', null=True, blank=True)
    service_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.service_name

class ServiceProvider(models.Model):
    user_as_a_provider = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    location = models.CharField(max_length=20)
    services_provided = models.ManyToManyField(Service, blank=True)  # Establish a many-to-many relationship with Service

    def __str__(self):
        return f"{self.user_as_a_provider.username}"

class ClientFeedback(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # ForeignKey to associate feedback with a specific service
    client_feedback = models.TextField()

    def __str__(self):
        return self.client_feedback

class Logo(models.Model):
    logo = models.ImageField(upload_to='logoimage', null=True, blank=True)
