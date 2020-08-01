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
