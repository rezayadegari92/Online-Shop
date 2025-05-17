from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views import View

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile2.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auth_token'] = self.request.session.get('auth_token', '')
        return context
    

class RegistrationView(View):
    def get(self, request):
        return render(request, 'register.html')
    


from django.shortcuts import render

def login_page(request):
    return render(request, 'login.html')
