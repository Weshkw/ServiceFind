from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('serviceproviderregistration/', views.register_service_provider, name='register_service_provider'),
    path('login/', views.login_view, name='login'),
    path('serviceprovider/', views.service_provider_latest_service, name='service_provider_services'),
    path('serviceproviderprofile/<int:pk>/', views.serviceproviderprofile,name='serviceproviderprofile'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),

]

#Serving static during development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)