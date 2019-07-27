from django.views.generic import CreateView
from django.views.generic import CreateView

from .forms import UserAdminCreationForm
from .models import User


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('home')


register = RegisterView.as_view()
