from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.db import transaction

from .models import User,Developer,ProjectManager,Ticket

class DeveloperSignupForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    
    def save(self):
        user = super().save(commit=False)
        user.is_developer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if User.objects.filter(email=user.email).exists():
            raise forms.ValidationError("Email is not unique")
        user.save()
        developer = Developer.objects.create(user=user)
        developer.phone_number=self.cleaned_data.get('phone')
        developer.save()
        return user
    

class ProjectManagerSignupForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)


    class Meta(UserCreationForm.Meta):
        model = User

    
    def save(self):
        user = super().save(commit=False)
        user.is_manager = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if User.objects.filter(email=user.email).exists():
            raise forms.ValidationError("Email is not unique")
        user.save()
        manager = ProjectManager.objects.create(user=user)
        manager.age=self.cleaned_data.get('age')
        manager.save()
        return user


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('ticket_title', 'ticket_description')


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('ticket_title', 'created_by', 'ticket_description',
                  'status', 'accepted_by')