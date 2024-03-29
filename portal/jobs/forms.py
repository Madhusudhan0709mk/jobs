# forms.py
from django import forms
from .models import Profile,createjobposts,contact

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','image' ]  # Add other fields as needed
        


class createjobpostsForm(forms.ModelForm):
    class Meta:
        model = createjobposts
        fields = ['companyname', 'cgpa', 'skills', 'address', 'email', 'about','created_at']
        
class contactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['name','email','message']
