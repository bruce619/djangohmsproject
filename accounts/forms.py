from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from accounts.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'email', 'is_staff', 'is_admin', 'password1', 'password2', )
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email',
            'is_staff': 'Is a staff',
            'is_admin': 'Is an Admin',
            'password1': 'Password',
            'password2': 'Confirm Password'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }
            ),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'is_staff': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'is_admin': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


class AccountAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("Invalid Email or Password")
            elif not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            elif not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(AccountAuthenticationForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'email',)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % account)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)