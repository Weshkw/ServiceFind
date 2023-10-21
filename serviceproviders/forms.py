from django import forms
from .models import CustomUser, ServiceProvider, Service

'''

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'email'}),
            'password': forms.PasswordInput(attrs={'class': 'password'}),
        }


    password2 = forms.CharField(required=True, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'password2'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password1
    


    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'profile_picture'}))
    location = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'location'}))
    service_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'service_name '}))
    service_charge = forms.DecimalField(max_digits=8, decimal_places=2, widget=forms.TextInput(attrs={'class': 'service_charge'}))
    service_video = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'service_video'}))
    service_picture = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'service_picture'}))
    service_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'service_description'}), required=False)

    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("Form is not valid. Cannot save.")

        # Create a CustomUser instance and set the user's attributes
        custom_user = super().save(commit=False)
        custom_user.set_password(self.cleaned_data['password'])

        # Create a ServiceProvider instance linked to the user
        service_provider = ServiceProvider(user_as_a_provider=custom_user) #This line creates a new ServiceProvider instance and associates it with the user specified by the custom_user instance.
        service_provider.location = self.cleaned_data['location']
        service_provider.profile_picture = self.cleaned_data['profile_picture']

        service = Service(
            service_name=self.cleaned_data['service_name'],
            service_charge=self.cleaned_data['service_charge'],
            service_video=self.cleaned_data['service_video'],
            service_picture=self.cleaned_data['service_picture'],
            service_description=self.cleaned_data['service_description']
        )

        if commit:
            custom_user.save()
            service_provider.save()
            service.save()
            service_provider.services_provided.add(service) # this line adds the FIRST SERVICE, to a list of services provided by the service provider

        return custom_user
    
'''





from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password2'}))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'profile_picture'}))
    location = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'service_name'}))
    service_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'location'}))
    service_charge = forms.DecimalField(max_digits=8, decimal_places=2, widget=forms.TextInput(attrs={'class': 'service_charge'}))
    service_video = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'service_video'}))
    service_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'service_picture'}))
    service_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'service_description'}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match")

        return cleaned_data








class CustomUserLoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'password'}), required=True)
