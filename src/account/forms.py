from account.models import User
from account.tasks import send_sign_up_email

from django import forms


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with given email exists!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError('Passwords do not match!')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.username = instance.email
        instance.is_active = False
        instance.set_password(self.cleaned_data['password1'])
        instance.save()

        send_sign_up_email(instance.id)
        return instance


class ChangePasswordForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = 'current_password', 'new_password', 'confirm_password'

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        if not new_password.isalnum():
            raise forms.ValidationError('The password must contain both numbers and letters!')
        elif new_password.islower():
            raise forms.ValidationError('The password must contain at least one uppercase letter!')
        else:
            return new_password

    def clean_password(self):
        password = self.cleaned_data['current_password']
        if not self.user.check_password(password):
            raise forms.ValidationError('The password is incorrect!')

        return password

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['new_password'] != cleaned_data['confirm_password']:
                raise forms.ValidationError('Passwords must match!')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data['new_password'])
        instance.save()

        return instance
