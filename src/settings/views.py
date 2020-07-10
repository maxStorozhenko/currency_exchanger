from account.forms import ChangePasswordForm
from account.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)


class ChangePassword(LoginRequiredMixin, UpdateView):
    template_name = 'password-change.html'
    model = User
    success_url = reverse_lazy('index')
    form_class = ChangePasswordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
