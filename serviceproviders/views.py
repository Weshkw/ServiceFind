import os
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from moviepy.editor import VideoFileClip

from .forms import RegistrationForm, CustomUserLoginForm
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render,redirect
from .models import Logo,ServiceProvider, Service,CustomUser,ClientFeedback
from django.db import transaction
from django.views.decorators.http import require_POST
from PIL import Image
from moviepy.editor import VideoFileClip


def home(request):
    latest_logo = Logo.objects.order_by('-pk').first()
    service_providers = ServiceProvider.objects.all()
    context ={'logo': latest_logo,'service_providers':service_providers}
    return render(request, 'serviceproviders\home.html',context)

def service_provider_latest_service(request):
    service_providers = ServiceProvider.objects.all()
    context ={'service_providers':service_providers}
    return render(request, 'serviceproviders/home.html', context)


@require_POST
def submit_feedback(request):
    service_id = request.POST.get('service_id')
    client_feedback_text = request.POST.get('client_feedback')
    service = Service.objects.get(id=service_id)
    
    # Get the authenticated user's username or 'Anonymous' for anonymous users
    user_username = request.user.username if request.user.is_authenticated else 'Anonymous'
    
    if client_feedback_text:
        feedback = ClientFeedback(service=service, client_feedback=f" {user_username}: {client_feedback_text}")
        feedback.save()
        return redirect('home')

    return render(request, 'serviceproviders\home.html')

def serviceproviderprofile(request,pk):
    service_providers = ServiceProvider.objects.get(pk=pk)
    
    context={'service_providers': service_providers}


    return render(request, 'serviceproviders\profile.html',context)

def service_detail(request,pk):
    # Retrieve the specific service and its client feedback
    service = Service.objects.get(pk=pk)
    feedback = ClientFeedback.objects.filter(service=service)

    context = {
        'service': service,
        'feedback': feedback,
    }

    return render(request, 'service_detail.html', context)










def compress_video(video_file, width=640):
    # Load the video using VideoFileClip
    video = VideoFileClip(video_file)
    # Resize the video width to the specified value
    video = video.resize(width=width)
    
    # Save the compressed video to an in-memory file
    with BytesIO() as output_buffer:
        video.write_videofile(output_buffer, codec='libx264')
        compressed_video = ContentFile(output_buffer.getvalue())
    
    return compressed_video
from moviepy.editor import VideoFileClip


def register_service_provider(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            # Extract data from the form
            with transaction.atomic():
                
                # Extract data from the form
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                profile_picture = form.cleaned_data['profile_picture']
                location = form.cleaned_data['location']
                service_name = form.cleaned_data['service_name']
                service_charge = form.cleaned_data['service_charge']
                service_video = form.cleaned_data['service_video']
                service_picture = form.cleaned_data['service_picture']
                service_description = form.cleaned_data['service_description']

                # Create user instance
                user = CustomUser(username=username, email=email)
                user.set_password(password)
                user.save()


                #if service_video:
                    #service_video = compress_video(service_video)

                # Create service instance
                service = Service.objects.create(
                    service_name=service_name,
                    service_charge=service_charge,
                    service_video=service_video,
                    service_picture=service_picture,
                    service_description=service_description
                )

                # Create service provider
                provider = ServiceProvider.objects.create(
                    user_as_a_provider=user,
                    profile_picture=profile_picture,
                    location=location
                )

                # Add the service to the provider using .set()
                provider.services_provided.set([service])

                return redirect('home')  # Redirect to a success page if everything is successful

    else:
        form = RegistrationForm()

    return render(request, 'serviceproviders\service_provider_registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or do something else
                return redirect('home')
    else:
        form = CustomUserLoginForm()

    return render(request, 'serviceproviders\login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
