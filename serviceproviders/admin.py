from django.contrib import admin
from .models import CustomUser, Service, ServiceProvider, ClientFeedback

# Create an admin class for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomUser._meta.fields]
    search_fields = [field.name for field in CustomUser._meta.fields]

# Create an admin class for Service
class ServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Service._meta.fields]
    search_fields = [field.name for field in Service._meta.fields]

# Create an admin class for ServiceProvider
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ServiceProvider._meta.fields]
    search_fields = [field.name for field in ServiceProvider._meta.fields]

# Create an admin class for ClientFeedback
class ClientFeedbackAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ClientFeedback._meta.fields]
    search_fields = [field.name for field in ClientFeedback._meta.fields]

# Register the models with their respective admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(ClientFeedback, ClientFeedbackAdmin)
