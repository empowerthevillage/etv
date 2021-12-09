from django import template
from django.shortcuts import render
from mailchimp_marketing import Client
from django.conf import settings
from etv.forms import MailchimpForm
import sweetify

mailchimp = Client()
mailchimp.set_config({
    "api_key": settings.MAILCHIMP_API_KEY,
    "server": "us7"
})

register = template.Library()

@register.inclusion_tag('base.html', takes_context=True)
def mailchimp_request(context):
    request = context['request']

    if request.method == 'POST':
        mailchimp_form = MailchimpForm(request.POST)
        if mailchimp_form.is_valid():
            email = mailchimp_form.cleaned_data['email']
            mailchimp.lists.add_list_member('bfb104d810', email)
            sweetify.success(request, title='Thank you!', icon='success', text='Thank you for joining the ETV mailing list!', button='OK', timer=3000)
            context = {
                'mailchimp_form': mailchimp_form,
            }
        return render(request, 'base.html', context)

@register.inclusion_tag('base.html', takes_context=True)
def mailchimp_post(context):
    mailchimp_form = context['mailchimp_form']
    return render('base.html', context)