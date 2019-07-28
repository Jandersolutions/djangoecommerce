from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import ContactForm

User = get_user_model()


class HomeView(TemplateView):
    template_name = 'index.html'


home = HomeView.as_view()


def contato(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            message = 'Nome:{0}\nE-mail:{1}\n{2}'.format(name, email, message)
            send_mail('Contato do django-ecommerce', message, settings.DEFAULT_FROM_EMAIL,
                      [settings.DEFAULT_FROM_EMAIL]

                      )
            success = True
        elif request.method == 'POST':
            messages.error(request, 'Formulário invalido')
    form = ContactForm()
    context = {
        'form': form,
        'success': success
    }
    return render(request, 'contact.html', context)

# class RegisterView(CreateView):
#     form_class = UserCreationForm
#     template_name = 'register.html'
#     model = User
#     success_url = reverse_lazy('home')
# register = RegisterView.as_view()
