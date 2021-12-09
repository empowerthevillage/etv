from accounts.forms import LoginForm
from .forms import MailchimpForm

def add_login_form(request):
    return {
        'login_form': LoginForm(request)
    }

