from .forms import RegistrationForm, CustomUserLoginForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect
from .models import Logo,ServiceProvider, Service,CustomUser,ClientFeedback
from django.db import transaction
from django.contrib import messages


def home(request):
    latest_logo = Logo.objects.order_by('-pk').first()
    service_providers = ServiceProvider.objects.all()
    context ={'logo': latest_logo,'service_providers':service_providers}
    return render(request, 'serviceproviders\home.html',context)

def service_provider_latest_service(request):
    service_providers = ServiceProvider.objects.all()
    context ={'service_providers':service_providers}
    return render(request, 'serviceproviders/home.html', context)

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