from django.shortcuts import render, redirect
from .forms import BusinessForm
from .models import FamilyNomination, Nomination
import sweetify

def venForm(request):
    if request.method == 'POST':
        if request.POST.get('submission-type') == 'business':
            nomination_form = BusinessForm(request.POST)
            obj = Nomination()
            obj.nominator_name = nomination_form.data['nominator-name']
            obj.nominator_email = nomination_form.data['nominator-email']
            obj.owner_name = nomination_form.data['owner-name']
            obj.business_name = nomination_form.data['business_name']
            obj.website = nomination_form.data['website']
            obj.city = nomination_form.data['city']
            obj.state = nomination_form.data['state']
            obj.phone = nomination_form.data['phone']
            obj.category = nomination_form.data['category']
            obj.subcategory = nomination_form.data['subcategory']
            obj.nominator_owner = nomination_form.data['owned']
            obj.years_in_business = nomination_form.data['years-active']
            obj.employees = nomination_form.data['employees']
            obj.revenue = nomination_form.data['revenue']
            obj.structure = nomination_form.data['structure']
            obj.priority1 = nomination_form.data['priority1']
            obj.other1 = nomination_form.data['other1-custom']
            obj.priority2 = nomination_form.data['priority2']
            obj.other2 = nomination_form.data['other2-custom']
            obj.priority3 = nomination_form.data['priority3']
            obj.other3 = nomination_form.data['other3-custom']
            obj.instagram = nomination_form.data['instagram']
            obj.facebook = nomination_form.data['facebook']
            obj.twitter = nomination_form.data['twitter']
            obj.save()
            sweetify.success(request, title='Thank you!', icon='success', text="Thank you for registering for the Village Empowerment Network!", button='OK', timer=6000)

        elif request.POST.get('submission-type') == 'family':
            form = request.POST
            obj = FamilyNomination()
            obj.name = form.get('name')
            obj.email = form.get('email')
            obj.phone = form.get('phone')
            obj.city = form.get('city')
            obj.state = form.get('state')
            obj.employment_status = form.get('employmentstatus')
            obj.age_range = form.get('age-range')
            obj.household_size = form.get('household-size')
            obj.income = form.get('income')
            obj.priority1 = form.get('priority1')
            obj.other1 = form.get('other1-custom')
            obj.priority2 = form.get('priority2')
            obj.other2 = form.get('other2-custom')
            obj.priority3 = form.get('priority3')
            obj.other3 = form.get('other3-custom')
            obj.save()
            sweetify.success(request, title='Thank you!', icon='success', text="Thank you for registering for the Village Empowerment Network!", button='OK', timer=6000)
        
        elif request.POST.get('submission-type') == 'both':
            form = request.POST

            business_obj = Nomination()
            individual_obj = FamilyNomination()

            business_obj.nominator_name = form.get('full-name-individual')
            business_obj.nominator_email = form.get('email-individual')
            business_obj.owner_name = form.get('owner-name')
            business_obj.business_name = form.get('business_name')
            business_obj.website = form.get('website')
            business_obj.city = form.get('city')
            business_obj.state = form.get('state')
            business_obj.phone = form.get('phone')
            business_obj.category = form.get('category')
            business_obj.subcategory = form.get('subcategory')
            business_obj.nominator_owner = form.get('owned')
            business_obj.years_in_business = form.get('years-active')
            business_obj.employees = form.get('employees')
            business_obj.revenue = form.get('revenue')
            business_obj.structure = form.get('structure')
            business_obj.priority1 = form.get('priority1')
            business_obj.other1 = form.get('other1-custom')
            business_obj.priority2 = form.get('priority2')
            business_obj.other2 = form.get('other2-custom')
            business_obj.priority3 = form.get('priority3')
            business_obj.other3 = form.get('other3-custom')
            business_obj.instagram = form.get('instagram')
            business_obj.facebook = form.get('facebook')
            business_obj.twitter = form.get('twitter')

            individual_obj.name = form.get('full-name-individual')
            individual_obj.email = form.get('email-individual')
            individual_obj.phone = form.get('phone-individual')
            individual_obj.city = form.get('city-individual')
            individual_obj.state = form.get('individual_state')
            individual_obj.employment_status = form.get('employmentstatus')
            individual_obj.age_range = form.get('age-range')
            individual_obj.household_size = form.get('household-size')
            individual_obj.income = form.get('income')
            individual_obj.priority1 = form.get('priority1-family')
            individual_obj.other1 = form.get('other1-custom-family')
            individual_obj.priority2 = form.get('priority2-family')
            individual_obj.other2 = form.get('other2-custom-family')
            individual_obj.priority3 = form.get('priority3-family')
            individual_obj.other3 = form.get('other3-custom-family')


            individual_obj.save()
            business_obj.save()

            sweetify.success(request, title='Thank you!', icon='success', text="Thank you for registering for the Village Empowerment Network!", button='OK', timer=6000)
        return redirect('/village-empowerment-network-nomination')
    else:
        nomination_form = BusinessForm()
    return render(
        request, 
        'ven-form.html', 
        {
        'title': 'ETV | Village Empowerment Network Registration Form',
        'nomination_form': nomination_form
        }
    )

def venFamilyForm(request):
    if request.method == 'POST':
        nomination_form = BusinessForm(request.POST)
        obj = Nomination()
        obj.nominator_name = nomination_form.data['nominator-name']
        obj.nominator_email = nomination_form.data['nominator-email']
        obj.owner_name = nomination_form.data['owner-name']
        obj.business_name = nomination_form.data['business_name']
        obj.website = nomination_form.data['website']
        obj.city = nomination_form.data['city']
        obj.phone = nomination_form.data['phone']
        obj.category = nomination_form.data['category']
        obj.subcategory = nomination_form.data['subcategory']
        obj.nominator_owner = nomination_form.data['owned']
        obj.years_in_business = nomination_form.data['years-active']
        obj.employees = nomination_form.data['employees']
        obj.revenue = nomination_form.data['revenue']
        obj.structure = nomination_form.data['structure']
        obj.priority1 = nomination_form.data['priority1']
        obj.other1 = nomination_form.data['other1-custom']
        obj.priority2 = nomination_form.data['priority2']
        obj.other2 = nomination_form.data['other2-custom']
        obj.priority3 = nomination_form.data['priority3']
        obj.other3 = nomination_form.data['other3-custom']
        obj.nominator_recommended = nomination_form.data['recommended']
        obj.state = nomination_form.data['state']
        obj.instagram = nomination_form.data['instagram']
        obj.facebook = nomination_form.data['facebook']
        obj.twitter = nomination_form.data['twitter']
        obj.save()
        sweetify.success(request, title='Thank you!', icon='success', text='Thank you for nominating a Black-owned business!', button='OK', timer=4000)
        return redirect('/village-empowerment-network-nomination')
    else:
        nomination_form = BusinessForm()
    return render(
        request, 
        'family-form.html', 
        {
        'title': 'ETV | Village Empowerment Network Nomination Form',
        'nomination_form': nomination_form
        }
    )

def ven_home(request):
    context = {
        "title": "ETV | Village Empowerment Network"
    }
    return render(request, 'ven-home.html', context)
    
