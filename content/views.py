from django.shortcuts import redirect, render
from content.forms import ContactForm
from etv.forms import MailchimpForm
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from django.conf import settings
from content.models import contact_submission
from django.http import HttpResponse
import sweetify

mailchimp = Client()
mailchimp.set_config({
    "api_key": settings.MAILCHIMP_API_KEY,
    "server": "us7"
})

def efbf(request):
    context = {
    }
    return render(request, "efbf.html", context)

def efbf_subscribed(request):
    context = {
    }
    return render(request, "efbf_subscribed.html", context)

def contact(request):
    contact_form = ContactForm()
    if request.method == 'POST':
      contact = ContactForm(request.POST)
      obj = contact_submission()
      obj.name = contact.data['name']
      obj.email = contact.data['email']
      obj.message = contact.data['message']
      if request.user.is_authenticated:
        user = request.user
        obj.user = user
      obj.save()
      sweetify.success(request, title='Thank you!', icon='success', text="We'll be in touch!", button='OK', timer=4000)
    context = {
      'contact_form': contact_form 
    }
    return render(request, "contact.html", context)

def mailchimp_signup(request):
  if request.method == 'POST':
    print(request.POST)
    mailchimp_form = MailchimpForm(request.POST)
    if mailchimp_form.is_valid():
      member_info = {
        'email_address': mailchimp_form.cleaned_data["email"],
        'status': 'subscribed'
      }
      try:
        response = mailchimp.lists.add_list_member('bfb104d810', member_info)
        print("response: {}".format(response))
      except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
      
    return redirect('/make-every-friday-black-friday/')