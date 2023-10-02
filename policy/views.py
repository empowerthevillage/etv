from django.core.mail import send_mail
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .models import Flyer, VillageStriversApplication


import sweetify

CATEGORY_CHOICES = [
    ('beauty','Beauty & Personal Grooming'),
    ('books', 'Books & Publishing'),
    ('cars', 'Cars & Automotive'),
    ('child', "Childcare | Children's Services & Products"),
    ('cleaning', 'Cleaning'),
    ('clothing', 'Clothing & Fashion'),
    ('construction', 'Construction & Trades'),
    ('education', 'Education'),
    ('eldercare', 'Eldercare'),
    ('electronics', 'Electronics & Technology'),
    ('entertainment', 'Entertainment'),
    ('etv-nonprofit', 'ETV/Nonprofit'),
    ('farming', 'Farming & Agriculture'),
    ('florists', 'Florists'),
    ('grocery', 'Grocery & Food Services'),
    ('health', 'Health & Wellness'),
    ('home', 'Home & Garden'),
    ('hotels', 'Hotels & Hospitality | Travel'),
    ('jewelry', 'Jewelry & Accessories'),
    ('legal', 'Legal & Financial Services'),
    ('lifestyle', 'Lifestyle'),
    ('marketing', 'Marketing & Advertising'),
    ('medical', 'Medical Services'),
    ('packaging', 'Packaging | Delivery | Shipping'),
    ('pets', 'Pets & Animal Care'),
    ('photography', 'Photography & Video'),
    ('professional', 'Professional Services'),
    ('real estate', 'Real Estate'),
    ('recreation', 'Recreation & Sports'),
    ('restaurants', 'Restaurants & Bars | Event Spaces'),
    ('security', 'Security Services'),
    ('transportation', 'Transportation & Trucking'),
    ('visual', 'Visual & Performing Arts | Culture'),
    ('other', 'Other'),
]

def policy_home(request):
    context = {
        'title': 'ETV | Policy & Power',
    }
    return render(request, "policy_home.html", context)

def voting(request):
    context = {
        'title': 'ETV | Operation Ballot Box',
        'flyers': Flyer.objects.filter(active=True)
    }
    return render(request, "voting.html", context)

def voting_print(request):
    context = {
        'title': 'ETV | Operation Ballot Box',
    }
    return render(request, "voting_print.html", context)

def obb_flyer(request, state):
    published_states = ['az', 'tx', 'ar', 'la', 'ga', 'fl', 'nc', 'ky', 'oh', 'mi', 'wi', 'pa', 'md', 'nj']
    state_formatted = str(state).lower()
    if state_formatted in published_states:
        url = 'https://empowerthevillage.s3.amazonaws.com/static/img/operation-ballot-box/%s-web.pdf' %(state_formatted)
        return redirect(url)
    else:
        return redirect('/policy-and-power/voting/')
    
def strivers_application(request):
    if request.method == 'POST':
        print(request.FILES)
        app_obj = VillageStriversApplication()
        app_obj.first_name = request.POST['first_name']
        app_obj.last_name = request.POST['last_name']
        app_obj.email = request.POST['email']
        try:
            app_obj.resume = request.FILES['resume']
        except:
            pass
        try:
            app_obj.phone = request.POST['phone']
        except:
            pass
        app_obj.school_classification = request.POST['school-classification']
        app_obj.category = request.POST['category']
        try:
            app_obj.interest = request.POST['interest']
        except:
            pass
        try:
            app_obj.open_to_unpaid = request.POST['open_to_unpaid']
        except:
            pass
        app_obj.save()
        sweetify.success(request, title='Thank you!', icon='success', html="<p>ETV will contact you if there is a potential match for your interests. Email us at <a href='mailto:VillageStrivers@empowerthevillage.org'>VillageStrivers@EmpowerTheVillage.org</a></p>", persistent='OK')
        detail_content = render_to_string('strivers-admin-email.html',
        {
            'application': app_obj,
        })
        recipients = ['chandler@eliftcreations.com', 'admin@empowerthevillage.org', 'ayo@empowerthevillage.org', 'villagestrivers@empowerthevillage.org']
        #recipients = ['chandler@eliftcreations.com']
        send_mail(
            'New Village Strivers Application!',
            str('A new village Strivers Application has been received! '+ str(app_obj)),
            'etvnotifications@gmail.com',
            recipients,
            html_message=detail_content,
            fail_silently=True
        )
        return redirect('/education/village-strivers/')
    else: 
        context = {
            'title': 'ETV | Village Strivers Application',
            'categories': CATEGORY_CHOICES,
        }
        return render(request, "strivers_application.html", context)