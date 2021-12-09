from django.shortcuts import render, redirect
from .forms import BusinessForm
from .models import Nomination
import sweetify

def venForm(request):
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
        'ven-form.html', 
        {
        'title': 'ETV | Village Empowerment Network Nomination Form',
        'nomination_form': nomination_form
        }
    )
