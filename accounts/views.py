from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('pages:home')

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! Please login.')
        return response

class CustomLogoutView(LogoutView):
    next_page = 'pages:home'

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auth_token'] = self.request.session.get('auth_token', '')
        return context

class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.request.user.orders.all().order_by('-created_at')
