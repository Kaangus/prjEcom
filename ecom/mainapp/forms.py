from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class loginform(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

    class meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.fields['username'].label = 'login'
        self.fields['password'].password = 'password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = user.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f"incorrect username, can't found")
        if not user.check_password(password):
            raise forms.ValidationError(f"incorrect password")
        return self.cleaned_data

class registrationform(forms.Form):
    username = forms.CharField(required=true)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=true)
    first_name = forms.CharField(required=true)
    last_name = forms.CharField(required=true)

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.fields['username'].label = 'login'
        self.fields['password'].label = 'password'
        self.fields['confirm_password'].label = 'password confirmation'
        self.fields['email'].label = 'email'
        self.fields['first_name'].label = 'first name'
        self.fields['last_name'].label = 'last name'

    def clean_email(self):
        email = self.cleaned_data['email']
        email_check = email.split('.')[-1]
        if email_check not in ['ru', 'com', 'net']:
            raise forms.ValidationError(f"incorrect email address for {email_check}")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Email already registered")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Username already exists")
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError(f"Password and confirmation do not match")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'first_name', 'last_name']
