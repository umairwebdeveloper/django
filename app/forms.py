from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserProfile
import mimetypes

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        label="Password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        if len(password) < 8:
            self.add_error('password', "Password must be at least 8 characters long.")

        return cleaned_data
    

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=150, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['profile_image', 'id_card_front', 'id_card_back']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_card_front': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_card_back': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user instance
        super().__init__(*args, **kwargs)
        if user:
            # Populate user fields with initial data
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        # Save user fields first
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return super().save(commit)

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        return self.validate_image(image, "Profile image")

    def clean_id_card_front(self):
        image = self.cleaned_data.get('id_card_front')
        return self.validate_image(image, "ID Card Front")

    def clean_id_card_back(self):
        image = self.cleaned_data.get('id_card_back')
        return self.validate_image(image, "ID Card Back")

    def validate_image(self, image, field_name):
        if image:
            if image.size > 5 * 1024 * 1024:  # 5 MB
                raise ValidationError(f"{field_name} size should not exceed 5MB.")

            mime_type, _ = mimetypes.guess_type(image.name)
            if not mime_type or not mime_type.startswith('image'):
                raise ValidationError(f"{field_name} must be a valid image file.")
        return image