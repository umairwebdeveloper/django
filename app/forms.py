from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserProfile, PhoneNumber
from django.contrib.auth.password_validation import validate_password
import mimetypes

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter Email',
            'class': 'form-control',
            'autocomplete': 'new-email',
            'required': 'required',
        }),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'autocomplete': 'new-password',
            'required': 'required',
        }),
        label="Password",
    )
class StartUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'autocomplete': 'new-password',
            'required': 'required',
        }),
        label="Password",
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': 'required',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': 'required',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email',
                'required': 'required',
                'autocomplete': 'new-email',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if self.user_instance:
            self.fields['email'].initial = self.user_instance.email
            self.fields['email'].disabled = True  # Disable email field since it shouldn't be updated

    def clean_email(self):
        # Ensure email matches the associated user
        email = self.cleaned_data.get('email')
        if self.user_instance and email != self.user_instance.email:
            raise ValidationError("Email cannot be changed.")
        return email

    def save(self, commit=True):
        if not self.user_instance:
            raise ValueError("User instance must be provided to update the user.")
        
        # Update user fields
        user = self.user_instance
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.set_password(self.cleaned_data.get('password'))
        
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
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
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = [
            'profile_image',
            'id_card_front',
            'id_card_back',
            'street_name',
            'street_number',
            'city',
            'zip_code',
            'state',
        ]
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_card_front': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_card_back': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control'}),
            'street_number': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user instance
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            if hasattr(user, 'phone_number'):
                self.fields['phone_number'].initial = user.phone_number.number
        
        # Check the status of the profile and remove image upload fields if approved
        if self.instance.status == 'approved':
            for field in ['profile_image', 'id_card_front', 'id_card_back']:
                if field in self.fields:
                    self.fields.pop(field)

    def save(self, commit=True):
        # Save user fields first
        user = self.instance.user
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        user.save()
        phone_number = self.cleaned_data.get('phone_number')
        if hasattr(user, 'phone_number'):
            user.phone_number.number = phone_number
            user.phone_number.save()
        else:
            PhoneNumber.objects.create(user=user, number=phone_number)
        
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

    
from django.utils.crypto import get_random_string

class CustomUserCreationForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        # Validate that the email is unique
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        # Save the user with a randomly generated password
        user = super().save(commit=False)
        user.username = user.email  # Use the email as username
        random_password = get_random_string(12)  # Generate a random password
        user.set_password(random_password)
        user.generated_password = random_password  # Add this attribute for later use
        if commit:
            user.save()
        return user