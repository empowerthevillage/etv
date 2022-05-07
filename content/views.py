from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.mail import send_mail
from content.forms import ContactForm
from etv.forms import MailchimpForm
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from django.conf import settings
from content.models import contact_submission
from django.http import HttpResponse
import sweetify
import requests
import json

recaptcha_secret = settings.RECAPTCHA
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
      grecaptcha = request.POST.get('g-recaptcha-response')
      params = {'secret': str(recaptcha_secret), 'response': grecaptcha}
      if grecaptcha != '':
          r = requests.post('https://www.google.com/recaptcha/api/siteverify', data = params)
          response = json.loads(r.content)
          if response['success'] == False:
              sweetify.toast(request, "Invalid RECAPTCHA, please try again!", icon="error", timer=5000)
          elif response['success'] == True:
              obj = contact_submission()
              obj.name = contact.data['name']
              obj.email = contact.data['email']
              obj.message = contact.data['message']
              if request.user.is_authenticated:
                user = request.user
                obj.user = user
              obj.save()
              detail_content = render_to_string('contact-admin-email.html',
              {
                  'name': obj.name,
                  'email': obj.email,
                  'message': obj.message,
              })
              recipients = ['chandler@eliftcreations.com', 'admin@empowerthevillage.org', 'ayo@empowerthevillage.org']
              send_mail(
                  'New Contact Us Request',
                  str('A new contact request has been received from'+ str(obj.name)),
                  'etvnotifications@gmail.com',
                  recipients,
                  #['chandler@eliftcreations.com'],
                  html_message=detail_content,
                  fail_silently=True
              )
              sweetify.success(request, title='Thank you!', icon='success', text="We'll be in touch!", button='OK', timer=4000)
      else:
            sweetify.toast(request, "We want to make sure you're a human! Please complete the RECAPTCHA", icon="error", timer=3000)        
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