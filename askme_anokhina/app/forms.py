import django
from django import forms
from django.forms import PasswordInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from app.models import Profile, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=5, widget=PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrongpassword':
            raise ValidationError('wrong passwod value!')
        
        return data
    

class RegistrationForm(forms.ModelForm):
    password_check = forms.CharField(min_length=5, widget=PasswordInput)
    password = forms.CharField(min_length=5, widget=PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def clean(self):
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_check')

        if password_1 != password_2:
            raise ValidationError('Passwords do not match!')
        
        return self.cleaned_data
    
    def save(self):
        self.cleaned_data.pop('password_check')
        
        user = User.objects.create_user(**self.cleaned_data)
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        return user


class SettingsForm(forms.ModelForm):
    #avatar = forms.ImageField(required=False)
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'avatar']

    
    def save(self, *args, **kwargs):
        user = super().save()
        #user.set_password(user.password)
        # user.save()

        profile = user.profile
        profile.avatar = self.cleaned_data['avatar']
        profile.save()

        return user


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']