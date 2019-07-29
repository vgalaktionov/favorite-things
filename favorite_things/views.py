from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect, reverse
from django.views.generic import TemplateView
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)

    def __init__(self, request, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data['username'])
        login(self.request, user)
        return HttpResponseRedirect(reverse('index'))


class FrontendView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().get(request, *args, **kwargs)
