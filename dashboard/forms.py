from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

mailchimp = Client()
mailchimp.set_config({
    "api_key": settings.MAILCHIMP_API_KEY,
    "server": "us7"
})

User = get_user_model()

from .models import MyUser, GuestEmail
from .signals import user_logged_in

class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse("account:register")
            msg = """This email is not associated with an account, would you like to <a href="{link}">register</a>?
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
            return email
        return email

class GuestForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={'class':'form-control'}), label_suffix='')
    class Meta:
        model = GuestEmail
        fields = [
            'email'
        ]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GuestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        # Save the provided password in hashed format
        obj = super(GuestForm, self).save(commit=False)
        if commit:
            obj.save()
            request = self.request
            request.session['guest_email_id'] = obj.id
        return obj

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={'class':'textfield'}), label_suffix='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'textfield'}), label_suffix='')

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is None:
            print(user)
            msg4 = "Incorrect Email Address or Password"
            raise forms.ValidationError(mark_safe(msg4))
        login(request, user)
        self.user = user
        user_logged_in.send(user.__class__, instance=user, request=request)
        try:
            del request.session['guest_email_id']
        except:
            pass
        return data

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='')
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='')
    
    class Meta:
        model = MyUser
        fields = ('username','email', 'password1', 'password2', 'first_name', 'last_name')

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email','username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        member_info = {
            'email_address': user.email,
            'status': 'subscribed'
        }
        try:
            response = mailchimp.lists.add_list_member('bfb104d810', member_info)
            print("response: {}".format(response))
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'password', 'admin',)

    def clean_password(self):
        return self.initial["password"]

class UserTeamForm(forms.ModelForm):
    team = forms.CharField(label='Team', widget=forms.TextInput(attrs={'class':'textfield'}), label_suffix='')
    class Meta:
        model=User
        fields=['team']
