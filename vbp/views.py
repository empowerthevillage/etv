import django
from django.db.models import query, F
from django.core.serializers import serialize
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from bfchallenge.models import STATE_CHOICES
from .models import vbp, vbp_book, vbp_al, vbp_az, vbp_az, vbp_ar, vbp_ca, vbp_co, vbp_ct, vbp_de, vbp_dc, vbp_fl, vbp_ga, vbp_hi, vbp_id, vbp_il, vbp_in, vbp_ia, vbp_ks, vbp_ky, vbp_la, vbp_me, vbp_md, vbp_ma, vbp_mi, vbp_mi, vbp_ms, vbp_mn, vbp_mo, vbp_mt, vbp_ne, vbp_nv, vbp_nh, vbp_nj, vbp_nm, vbp_ny, vbp_nc, vbp_nd, vbp_oh, vbp_ok, vbp_or, vbp_pa, vbp_ri, vbp_sc, vbp_sd, vbp_tn, vbp_tx, vbp_ut, vbp_vt, vbp_va, vbp_wa, vbp_wv, vbp_wi, vbp_wy  
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .forms import NominationForm
from django.db.models import Count
from .models import StateFilter
import sweetify

import json
import django_filters
import geocoder

BEAUTY_CHOICES = {
    "barber": 'Barber',
    "bathandbody": 'Bath & Body',
    "beautysalon": 'Beauty Salon',
    "beautysupply": 'Beauty Supply/Hair & Accessories', 
    "cosmetics": 'Cosmetics', 
    "nails": 'Nails',
    "travelingstylist": 'Traveling Stylist', 
    "other": 'Other',
}
BOOK_CHOICES = (
    ("bookstore", "Book Store"),
    ("onlinepub", "Online Publication"),
    ("publishing", "Publishing"),
    ("authors", "Authors"),
    ("other", "Other"),
)
CARS_CHOICES = (
    ("autodealership", "Auto Dealership"),
    ("autorepair", "Auto Repair/ Services"),
    ("carwash", "Car Wash"),
    ("gasstation", "Gas Station"),
    ("other", "Other"),
)
CHILD_CHOICES = (
    ("babyproducts", "Baby Products"),
    ("childcare", "Childcare/Daycare/ Preschool"),
    ("childbooks", "Children’s Books"),
    ("childactivities", "Children’s Activities"),
    ("other", "Other"),
)
CLEANING_CHOICES = (
    ("cleaningproducts", "Cleaning Products"),
    ("drycleaning", "Dry Cleaning"),
    ("laundry", "Laundry"),
    ("other", "Other"),
)
CLOTHING_CHOICES = (
    ("apparel", "Apparel"),
    ("stylist", "Stylist"),
    ("footwear", "Footwear"),
    ("fabric", "Fabric/Yarn"),
    ("other", "Other"),
)
CONSTRUCTION_CHOICES = (
    ("appliancerepair", "Appliance Repair"),
    ("construction", "Construction/ Engineering"),
    ("electrical", "Electrical"),
    ("hvac", "HVAC"),
    ("plumbing", "Plumbing"),
    ("powerwashing", "Power Washing"),
    ("roofing", "Roofing & Siding"),
    ("paintingservices", "Painting Services"),
    ("other", "Other"),
)
EDUCATION_CHOICES = (
    ("tutor", "Tutoring/ Academic Planning"),
    ("driving", "Driving/ Aviation"),
    ("enrichment", "Enrichment"),
    ("other", "Other"),
)
ELDERCARE_CHOICES = (
    ("assistedliving", "Assisted Living/Nursing Home"),
    ("homehealth", "Home Health Care/ Nursing Services"),
    ("adultdaycare", "Adult Day Care Center"),
    ("other", "Other"),
)
ELECTRONICS_CHOICES = (
    ("cybersecurity", "Cybersecurity"),
    ("software", "Software Development"),
    ("techsupport", "Tech Support/ Repair"),
    ("techproducts", "Tech Products"),
    ("webservices", "Web Services"),
    ("other", "Other"),
)
ENTERTAINMENT_CHOICES = (
    ("bands", "Bands/DJs/Performers"),
    ("comedian", "Comedian"),
    ("eventplanning", "Event Planning/Services"),
    ("media", "Media"),
    ("paintnsip", "Paint & Sip"),
    ("other", "Other"),
)
FARMING_CHOICES = (
    ("farmersmarket", "Farmer’s Market"),
    ("vineyard", "Vineyard"),
    ("other", "Other"),
)
GROCERY_CHOICES = (
    ("bakery", "Bakery"),
    ("catering", "Catering/ Chef"),
    ("coffee", "Coffee/Tea/Beverages"),
    ("fooddelivery", "Food Delivery Service"),
    ("icecream", "Ice Cream Parlor"),
    ("alcohol", "Alcohol"),
    ("specialty", "Specialty"),
    ("other", "Other"),
)
HEALTH_CHOICES = (
    ("addiction", "Addiction Treatment"),
    ("chiropractor", "Chiropractor"),
    ("fitness", "Fitness/ Yoga"),
    ("spa", "Spa/ Massage Therapy"),
    ("mentalhealth", "Mental Health Support"),
    ("nutrition", "Nutrition"),
    ("other", "Other"),
)
HOME_CHOICES = (
    ("furniture", "Furniture"),
    ("landscaping", "Landscaping/Gardening"),
    ("interiordesign", "Interior Design/ Home Staging"),
    ("pestcontrol", "Pest Control"),
    ("homegoods", "Home Goods/Décor"),
    ("other", "Other"),
)
HOTEL_CHOICES = (
    ("travelagent", "Travel Agent"),
    ("hospitality", "Hospitality/Hotels/Inns"),
    ("tours", "Tours"),
    ("other", "Other"),
)
JEWELRY_CHOICES = (
    ("accessories", "Accessories/ Handbags"),
    ("finejewelry", "Fine Jewelry"),
    ("other", "Other"),
)
LEGAL_CHOICES = (
    ("financialservices", "Financial Services"),
    ("notary", "Notary"),
    ("bail", "Bail Bonds Service"),
    ("legal", "Legal Services (General)"),
    ("realestatelaw", "Real Estate Law"),
    ("estateplanning", "Estate Planning/Wills"),
    ("corporatelaw", "Corporate Law"),
    ("insurance", "Insurance"),
    ("other", "Other"),
)
LIFESTYLE_CHOICES = (
    ("adultnovelties", "Adult Novelties"),
    ("cbd", "CBD Products"),
    ("smoking", "Smoking & Paraphernalia"),
    ("tarot", "Tarot"),
    ("piercing", "Piercing/ Tattoos"),
    ("other", "Other"),
)
MARKETING_CHOICES = (
    ("advertising", "Advertising"),
    ("branding", "Branding/ Graphic Design"),
    ("marketing", "Marketing/ Digital Marketing"),
    ("webservices", "Web Services/ Social Media"),
    ("other", "Other"),
)
MEDICAL_CHOICES = (
    ("dental", "Dental/ Orthodontics"),
    ("medbilling", "Medical Billing"),
    ("physicaltherapy", "Physical Therapy"),
    ("speechpath", "Speech Pathologist"),
    ("diagnostic", "Diagnostic Testing/Labs"),
    ("vision", "Vision"),
    ("healthproducts", "Healthcare Products"),
    ("primarycare", "Primary Care"),
    ("obgyn", "OB/GYNs"),
    ("pediatrics", "Pediatrics"),
    ("dermatology", "Dermatology"),
    ("psychiatry", "Psychiatry/Mental Health"),
    ("other", "Other"),
)
OTHER_CHOICES = (
    ("antiques", "Antiques & Collectibles"),
    ("guns", "Guns & Shooting Ranges"),
    ("gifts", "Gifts & Stationery"),
    ("mortuary", "Mortuary/ Funeral Services"),
    ("marketplace", "Marketplace"),
    ("translation", "Translation Services"),
    ("officesupplies", "Office Supplies"),
    ("other", "Other"),
)
PACKAGING_CHOICES = (
    ("courier", "Courier"),
    ("printing", "Printing"),
    ("shipping", "Shipping"),
    ("other", "Other"),
)
PETS_CHOICES = (
    ("dogtraining", "Dog Training"),
    ("petsitting", "Pet Sitting/ Walking"),
    ("vet", "Veterinarian"),
    ("petgrooming", "Pet Grooming"),
    ("other", "Other"),
)
PHOTOGRAPHY_CHOICES = (
    ("videography", "Videography"),
    ("photography", "Photography"),
    ("other", "Other"),
)
PROFESSIONAL_CHOICES = (
    ("consulting", "Consulting"),
    ("humanresources", "Human Resources"),
    ("it", "IT"),
    ("recruiting", "Recruiting/ Staffing"),
    ("privateinvestigator", "Private Investigator"),
    ("writingservices", "Writing Services"),
    ("speakers", "Speakers"),
    ("adminsupport", "Administrative Support"),
    ("other", "Other"),
)
REALESTATE_CHOICES = (
    ("developers", "Developers"),
    ("homeinspection", "Home Inspection"),
    ("mortgageconsulting", "Mortgage Consulting"),
    ("propertymanagement", "Property Management"),
    ("realestateagents", "Real Estate Agents/ Brokers"),
    ("titleservices", "Title Services"),
    ("other", "Other"),
)
RECREATION_CHOICES = (
    ("arcade", "Arcade/Laser Tag"),
    ("sports", "Sports"),
    ("martialarts", "Martial Arts"),
    ("sportsequipment", "Sports Equipment"),
    ("pooltables", "Pool Tables"),
    ("gaming", "Gaming"),
    ("other", "Other"),
)
RESTAURANT_CHOICES = (
    ("bar", "Bar/Night Club"),
    ("bbq", "BBQ/ Soul Food Restaurant"),
    ("cafe", "Café"),
    ("caribbean", "Caribbean Restaurant"),
    ("creole", "Creole/Cajun Restaurant"),
    ("ethiopian", "Ethiopian/Eritrean Restaurant"),
    ("venues", "Venues/Event Spaces"),
    ("westafrican", "West African Restaurant"),
    ("foodtrucks", "Food Trucks/Carts"),
    ("other", "Other"),
)
TRANSPORTATION_CHOICES = (
    ("commuter", "Commuter/Shuttle Services"),
    ("mortuarytransport", "Mortuary Transport"),
    ("moving", "Moving Services"),
    ("parking", "Parking"),
    ("taxi", "Taxi"),
    ("limo", "Limo/ Party Bus"),
    ("trucking", "Trucking"),
    ("valet", "Valet"),
    ("other", "Other"),
)
VISUAL_CHOICES = (
    ("artgallery", "Art Gallery/ Museum"),
    ("dance", "Dance Studios/Lessons"),
    ("artists", "Artists"),
    ("theater", "Theater/Acting Lessons"),
    ("music", "Music Lessons/Instruments"),
    ("other", "Other"),
)

def get_subcategories(request):
    category = request.GET['category']  
    qs = None
    if category == 'Beauty & Personal Grooming':
        data = {
            "barber": 'Barber',
            "bathandbody": 'Bath & Body',
            "beautysalon": 'Beauty Salon',
            "beautysupply": 'Beauty Supply/Hair & Accessories', 
            "cosmetics": 'Cosmetics', 
            "nails": 'Nails',
            "travelingstylist": 'Traveling Stylist', 
            "other": 'Other',
        }
    elif category == 'Books & Publishing':
        qs = BOOK_CHOICES
    elif category == "Cars & Automotive":
        qs = CARS_CHOICES
    elif category == "Childcare | Children's Services & Products":
        qs = CHILD_CHOICES
    elif category == "Cleaning":
        qs = CLEANING_CHOICES
    print(qs)
    return JsonResponse(data)

def get_counties_de(request):
    queryset = vbp_de.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", DE", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_ct(request):
    queryset = vbp_ct.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", CT", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_ny(request):
    queryset = vbp_ny.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", NY", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_nj(request):
    queryset = vbp_nj.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", NJ", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_ma(request):
    queryset = vbp_ma.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", MA", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_va(request):
    queryset = vbp_va.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", VA", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_oh(request):
    queryset = vbp_oh.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", OH", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_pa(request):
    queryset = vbp_pa.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", PA", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_md(request):
    queryset = vbp_md.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", MD", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_al(request):
    queryset = vbp_al.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", AL", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_ar(request):
    queryset = vbp_ar.objects.all()
    for i in queryset:
        if not i.county:
            try:
                city = i.city
                geocode_result = geocoder.google(city+", AR", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.county = county
                i.save()
                print(i.county)
            except:
                pass
    return HttpResponse('Counties Got Got!')

def get_counties_il(request):
    queryset = vbp_il.objects.all()
    for i in queryset:
        if not i.county:
            city = i.city
            geocode_result = geocoder.google(city+", IL", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
            county = geocode_result.current_result.county
            i.county = county
            i.save()
            print(i.county)
    return HttpResponse('Counties Got Got!')

def get_counties_in(request):
    queryset = vbp_in.objects.all()
    for i in queryset:
        if not i.county:
            try:
                city = i.city
                geocode_result = geocoder.google(city+", IN", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.county = county
                i.save()
                print(i.county)
            except:
                pass
    return HttpResponse('Counties Got Got!')

def get_counties_la(request):
    queryset = vbp_la.objects.all()
    for i in queryset:
        if not i.county:
            try:
                city = i.city
                geocode_result = geocoder.google(city+", LA", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.county = county
                i.save()
                print(i.county)
            except:
                pass
    return HttpResponse('Counties Got Got!')

def get_counties_mi(request):
    queryset = vbp_mi.objects.all()
    for i in queryset:
        if not i.county:
            try:
                city = i.city
                geocode_result = geocoder.google(city+", MI", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.county = county
                i.save()
                print(i.county)
            except:
                pass
    return HttpResponse('Counties Got Got!')

def get_counties_ms(request):
    queryset = vbp_ms.objects.all()
    for i in queryset:
        if not i.county:
            try:
                city = i.city
                geocode_result = geocoder.google(city+", MS", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.county = county
                i.save()
                print(i.county)
            except:
                pass
    return HttpResponse('Counties Got Got!')

def get_counties_mo(request):
    queryset = vbp_mo.objects.all()
    for i in queryset:
        if not i.county:
            try:
                city = i.city
                geocode_result = geocoder.google(city+", MO", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.county = county
                i.save()
                print(i.county)
            except:
                pass
    return HttpResponse('Counties Got Got!')

def get_counties_sc(request):
    queryset = vbp_sc.objects.all()
    for i in queryset:
        if not i.county:
            try:
                city = i.city
                geocode_result = geocoder.google(city+", SC", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.county = county
                i.save()
                print(i.county)
            except:
                pass
    return HttpResponse('Counties Got Got!')

def get_counties_tn(request):
    queryset = vbp_tn.objects.all()
    for i in queryset:
        if not i.county:
            try:
                city = i.city
                geocode_result = geocoder.google(city+", TN", key='AIzaSyA1gqlqRGpMKsBiAKi9r0Q9b-v-BRDOL5k')
                county = geocode_result.current_result.county
                i.county = county
                i.save()
                print(i.county)
            except:
                pass
    return HttpResponse('Counties Got Got!')

def ct_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_ct.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_ct.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            })

def al_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_al.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_al.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }) 

def ar_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_ar.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_ar.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            })
 
def il_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_il.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_il.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            })
 
def in_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_in.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_in.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            })
 
def la_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_la.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_la.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            })
 
def mi_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_mi.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_mi.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            })
 
def mo_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_mo.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_mo.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            })
 
def ms_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_ms.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_ms.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            })
 
def sc_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_sc.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_sc.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            })
 
def tn_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_tn.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_tn.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            })
 
def ny_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_ny.objects.all())
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_ny.objects.all()
    for object in filtered_qs:
        obj = object
        print(obj)
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )

def nj_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_nj.objects.all())
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_nj.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
                'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )

def ma_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_ma.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_ma.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
                'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )

def va_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_va.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_va.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
                'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )

def pa_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_pa.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_pa.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )

def oh_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_oh.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_oh.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
            'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )

def md_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_md.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_ct.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
                'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )

def dc_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_dc.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_dc.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
                'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )

def de_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_de.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('city', 'business_name')

    paginator_beauty = Paginator(beauty, 16)
    beauty_page = 6
    paginator_books = Paginator(books, 16)
    books_page = beauty_page + paginator_beauty.num_pages + 1
    paginator_cars = Paginator(cars, 16)
    cars_page = books_page + paginator_books.num_pages + 1
    paginator_child = Paginator(child, 16)
    child_page = cars_page + paginator_cars.num_pages + 1
    paginator_cleaning = Paginator(cleaning, 16)
    cleaning_page = child_page + paginator_child.num_pages + 1
    paginator_clothing = Paginator(clothing, 16)
    clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
    paginator_construction = Paginator(construction, 16)
    construction_page = clothing_page + paginator_clothing.num_pages + 1
    paginator_education = Paginator(education, 16)
    education_page = construction_page + paginator_construction.num_pages + 1
    paginator_eldercare = Paginator(eldercare, 16)
    eldercare_page = education_page + paginator_education.num_pages + 1
    paginator_electronics = Paginator(electronics, 16)
    electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
    paginator_entertainment = Paginator(entertainment, 16)
    entertainment_page = electronics_page + paginator_electronics.num_pages + 1
    paginator_farming = Paginator(farming, 16)
    farming_page = entertainment_page + paginator_entertainment.num_pages + 1
    paginator_florists = Paginator(florists, 16)
    florists_page = farming_page + paginator_farming.num_pages + 1
    paginator_grocery = Paginator(grocery, 16)
    grocery_page = florists_page + paginator_florists.num_pages + 1
    paginator_health = Paginator(health, 16)
    health_page = grocery_page + paginator_grocery.num_pages + 1
    paginator_home = Paginator(home, 16)
    home_page = health_page + paginator_health.num_pages + 1
    paginator_hotels = Paginator(hotels, 16)
    hotels_page = home_page + paginator_home.num_pages + 1
    paginator_jewelry = Paginator(jewelry, 16)
    jewelry_page = hotels_page + paginator_hotels.num_pages + 1
    paginator_legal = Paginator(legal, 16)
    legal_page = jewelry_page + paginator_jewelry.num_pages + 1
    paginator_lifestyle = Paginator(lifestyle, 16)
    lifestyle_page = legal_page + paginator_legal.num_pages + 1
    paginator_marketing = Paginator(marketing, 16)
    marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
    paginator_medical = Paginator(medical, 16)
    medical_page = marketing_page + paginator_marketing.num_pages + 1
    paginator_packaging = Paginator(packaging, 16)
    packaging_page = medical_page + paginator_medical.num_pages + 1
    paginator_pets = Paginator(pets, 16)
    pets_page = packaging_page + paginator_packaging.num_pages + 1
    paginator_photography = Paginator(photography, 16)
    photography_page = pets_page + paginator_pets.num_pages + 1
    paginator_professional = Paginator(professional, 16)
    professional_page = photography_page + paginator_photography.num_pages + 1
    paginator_realestate = Paginator(realestate, 16)
    realestate_page = professional_page + paginator_professional.num_pages + 1
    paginator_recreation = Paginator(recreation, 16)
    recreation_page = realestate_page + paginator_realestate.num_pages + 1
    paginator_restaurants = Paginator(restaurants, 16)
    restaurants_page = recreation_page + paginator_recreation.num_pages + 1
    paginator_security = Paginator(security, 16)
    security_page = restaurants_page + paginator_restaurants.num_pages + 1
    paginator_transportation = Paginator(transportation, 16)
    transportation_page = security_page + paginator_security.num_pages + 1
    paginator_visual = Paginator(visual, 16)
    visual_page = transportation_page + paginator_transportation.num_pages + 1
    paginator_other = Paginator(other, 16)
    other_page = visual_page + paginator_visual.num_pages + 1
    unfiltered_qs = vbp_de.objects.all()
    for object in filtered_qs:
        obj = object
        paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook_filtered.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'filtered_qs': filtered_qs,
                'unfiltered_qs': unfiltered_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )

def bookFilters(request):
    data = dict(request.GET)
    cities = request.GET.getlist('cities[]')
    categories = request.GET.getlist('categories[]')
    for city in cities:
        city_set = vbp_ct.objects.filter(city=city)
        for category in categories:
            category_set = city_set.objects.filter(approved=True).filter(category=category)
            print(category_set)
    return HttpResponse('success')

def home(request):
    f = StateFilter(request.GET, queryset=vbp_nj.objects.all())
    covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
    initial_qs = vbp_ct.objects.all()
    beautysc = BEAUTY_CHOICES
    booksc = BOOK_CHOICES
    carssc = CARS_CHOICES
    childsc = CHILD_CHOICES
    cleaningsc = CLEANING_CHOICES
    clothingsc = CLOTHING_CHOICES
    constructionsc = CONSTRUCTION_CHOICES
    educationsc = EDUCATION_CHOICES
    eldersc = ELDERCARE_CHOICES
    electrionicssc = ELECTRONICS_CHOICES 
    entertainmentsc = ENTERTAINMENT_CHOICES
    farmsc = FARMING_CHOICES
    grocerysc = GROCERY_CHOICES 
    healthsc = HEALTH_CHOICES
    homesc = HOME_CHOICES 
    hotelsc = HOTEL_CHOICES
    jewelrysc = JEWELRY_CHOICES 
    legalsc = LEGAL_CHOICES
    lifestylesc = LIFESTYLE_CHOICES
    marketingsc = MARKETING_CHOICES
    medicalsc = MEDICAL_CHOICES
    othersc = OTHER_CHOICES
    packagingsc = PACKAGING_CHOICES
    petsc = PETS_CHOICES
    photographysc = PHOTOGRAPHY_CHOICES
    professionalsc = PROFESSIONAL_CHOICES 
    realestatesc = REALESTATE_CHOICES
    recreationsc = RECREATION_CHOICES
    restaurantsc = RESTAURANT_CHOICES 
    transportationsc = TRANSPORTATION_CHOICES 
    visualsc = VISUAL_CHOICES 
    return render(
        request, 
        'vbp_list.html', 
        {
        'covers_qs': covers_qs,
        'title': 'ETV | Village Black Pages',
        'initial_qs': initial_qs,
        'filter': f,
        'beautysc': beautysc,
        'booksc' : booksc,
        'carssc' : carssc,
        'childsc' : childsc,
        'cleaningsc' : CLEANING_CHOICES,
        'clothingsc' : CLOTHING_CHOICES,
        'constructionsc' : CONSTRUCTION_CHOICES,
        'educationsc' : EDUCATION_CHOICES,
        'eldersc' : ELDERCARE_CHOICES,
        'electrionicssc' : ELECTRONICS_CHOICES,
        'entertainmentsc' : ENTERTAINMENT_CHOICES,
        'farmsc' : FARMING_CHOICES,
        'grocerysc' : GROCERY_CHOICES,
        'healthsc' : HEALTH_CHOICES,
        'homesc' : HOME_CHOICES,
        'hotelsc' : HOTEL_CHOICES,
        'jewelrysc' : JEWELRY_CHOICES,
        'legalsc' : LEGAL_CHOICES,
        'lifestylesc' : LIFESTYLE_CHOICES,
        'marketingsc' : MARKETING_CHOICES,
        'medicalsc' : MEDICAL_CHOICES,
        'othersc' : OTHER_CHOICES,
        'packagingsc' : PACKAGING_CHOICES,
        'petsc' : PETS_CHOICES,
        'photographysc' : PHOTOGRAPHY_CHOICES,
        'professionalsc' : PROFESSIONAL_CHOICES, 
        'realestatesc' : REALESTATE_CHOICES,
        'recreationsc' : RECREATION_CHOICES,
        'restaurantsc' : RESTAURANT_CHOICES ,
        'transportationsc' : TRANSPORTATION_CHOICES,
        'visualsc' : VISUAL_CHOICES
        }
    )

def home_copy(request):
    f = StateFilter(request.GET, queryset=vbp_nj.objects.all())
    covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
    initial_qs = vbp_ct.objects.all()
    beautysc = BEAUTY_CHOICES
    booksc = BOOK_CHOICES
    carssc = CARS_CHOICES
    childsc = CHILD_CHOICES
    cleaningsc = CLEANING_CHOICES
    clothingsc = CLOTHING_CHOICES
    constructionsc = CONSTRUCTION_CHOICES
    educationsc = EDUCATION_CHOICES
    eldersc = ELDERCARE_CHOICES
    electrionicssc = ELECTRONICS_CHOICES 
    entertainmentsc = ENTERTAINMENT_CHOICES
    farmsc = FARMING_CHOICES
    grocerysc = GROCERY_CHOICES 
    healthsc = HEALTH_CHOICES
    homesc = HOME_CHOICES 
    hotelsc = HOTEL_CHOICES
    jewelrysc = JEWELRY_CHOICES 
    legalsc = LEGAL_CHOICES
    lifestylesc = LIFESTYLE_CHOICES
    marketingsc = MARKETING_CHOICES
    medicalsc = MEDICAL_CHOICES
    othersc = OTHER_CHOICES
    packagingsc = PACKAGING_CHOICES
    petsc = PETS_CHOICES
    photographysc = PHOTOGRAPHY_CHOICES
    professionalsc = PROFESSIONAL_CHOICES 
    realestatesc = REALESTATE_CHOICES
    recreationsc = RECREATION_CHOICES
    restaurantsc = RESTAURANT_CHOICES 
    transportationsc = TRANSPORTATION_CHOICES 
    visualsc = VISUAL_CHOICES 
    return render(
        request, 
        'vbp_list copy.html', 
        {
        'covers_qs': covers_qs,
        'title': 'ETV | Village Black Pages',
        'initial_qs': initial_qs,
        'filter': f,
        'beautysc': beautysc,
        'booksc' : booksc,
        'carssc' : carssc,
        'childsc' : childsc,
        'cleaningsc' : CLEANING_CHOICES,
        'clothingsc' : CLOTHING_CHOICES,
        'constructionsc' : CONSTRUCTION_CHOICES,
        'educationsc' : EDUCATION_CHOICES,
        'eldersc' : ELDERCARE_CHOICES,
        'electrionicssc' : ELECTRONICS_CHOICES,
        'entertainmentsc' : ENTERTAINMENT_CHOICES,
        'farmsc' : FARMING_CHOICES,
        'grocerysc' : GROCERY_CHOICES,
        'healthsc' : HEALTH_CHOICES,
        'homesc' : HOME_CHOICES,
        'hotelsc' : HOTEL_CHOICES,
        'jewelrysc' : JEWELRY_CHOICES,
        'legalsc' : LEGAL_CHOICES,
        'lifestylesc' : LIFESTYLE_CHOICES,
        'marketingsc' : MARKETING_CHOICES,
        'medicalsc' : MEDICAL_CHOICES,
        'othersc' : OTHER_CHOICES,
        'packagingsc' : PACKAGING_CHOICES,
        'petsc' : PETS_CHOICES,
        'photographysc' : PHOTOGRAPHY_CHOICES,
        'professionalsc' : PROFESSIONAL_CHOICES, 
        'realestatesc' : REALESTATE_CHOICES,
        'recreationsc' : RECREATION_CHOICES,
        'restaurantsc' : RESTAURANT_CHOICES ,
        'transportationsc' : TRANSPORTATION_CHOICES,
        'visualsc' : VISUAL_CHOICES
        }
    )

def getStateListings(request):
    state = request.GET['state']
    if state == 'US-AL':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_al.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_al.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_al.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_al.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_al.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_al.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_al.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_al.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_al.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_al.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_al.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_al.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_al.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_al.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_al.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_al.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_al.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_al.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_al.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_al.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_al.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_al.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_al.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_al.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_al.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_al.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_al.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_al.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_al.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_al.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_al.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_al.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_al.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_al.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_al.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_al.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_al.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_al.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_al.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_al.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_al.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_al.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_al.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_al.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_al.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_al.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_al.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_al.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_al.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_al.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_al.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_al.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_al.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_al.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_al.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_al.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_al.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_al.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_al.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_al.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_al.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_al.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_al.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_al.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_al.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_al.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_al.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_al.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-AZ':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_az.objects.all().order_by('category', 'city', 'business_name')),
        beauty = list(vbp_az.objects.filter(approved=True).filter(category='beauty').order_by('city', 'business_name'))
        books = list(vbp_az.objects.filter(approved=True).filter(category='books').order_by('city', 'business_name'))
        cars = list(vbp_az.objects.filter(approved=True).filter(category='cars'))
        child = list(vbp_az.objects.filter(approved=True).filter(category='child'))
        cleaning = list(vbp_az.objects.filter(approved=True).filter(category='cleaning'))
        clothing = list(vbp_az.objects.filter(approved=True).filter(category='clothing'))
        construction = list(vbp_az.objects.filter(approved=True).filter(category='construction'))
        education = list(vbp_az.objects.filter(approved=True).filter(category='education'))
        eldercare = list(vbp_az.objects.filter(approved=True).filter(category='eldercare'))
        electronics = list(vbp_az.objects.filter(approved=True).filter(category='electronics'))
        entertainment = list(vbp_az.objects.filter(approved=True).filter(category='entertainment'))
        farming = list(vbp_az.objects.filter(approved=True).filter(category='farming'))
        florists = list(vbp_az.objects.filter(approved=True).filter(category='florists'))
        grocery = list(vbp_az.objects.filter(approved=True).filter(category='grocery'))
        health = list(vbp_az.objects.filter(approved=True).filter(category='health'))
        home = list(vbp_az.objects.filter(approved=True).filter(category='home'))
        hotels = list(vbp_az.objects.filter(approved=True).filter(category='hotels'))
        jewelry = list(vbp_az.objects.filter(approved=True).filter(category='jewelry'))
        legal = list(vbp_az.objects.filter(approved=True).filter(category='legal'))
        lifestyle = list(vbp_az.objects.filter(approved=True).filter(category='lifestyle'))
        marketing = list(vbp_az.objects.filter(approved=True).filter(category='marketing'))
        medical = list(vbp_az.objects.filter(approved=True).filter(category='medical'))
        other = list(vbp_az.objects.filter(approved=True).filter(category='other'))
        packaging = list(vbp_az.objects.filter(approved=True).filter(category='packaging'))
        pets = list(vbp_az.objects.filter(approved=True).filter(category='pets'))
        photography = list(vbp_az.objects.filter(approved=True).filter(category='photography'))
        professional = list(vbp_az.objects.filter(approved=True).filter(category='professional'))
        realestate = list(vbp_az.objects.filter(approved=True).filter(category='real estate'))
        recreation = list(vbp_az.objects.filter(approved=True).filter(category='recreation'))
        restaurants = list(vbp_az.objects.filter(approved=True).filter(category='restaurants'))
        security = list(vbp_az.objects.filter(approved=True).filter(category='security'))
        transportation = list(vbp_az.objects.filter(approved=True).filter(category='transportation'))
        visual = list(vbp_az.objects.filter(approved=True).filter(category='visual'))

        paginator_beauty = Paginator(beauty, 16)
        paginator_books = Paginator(books, 16)
        paginator_cars = Paginator(cars, 16)
        paginator_child = Paginator(child, 16)
        paginator_cleaning = Paginator(cleaning, 16)
        paginator_clothing = Paginator(clothing, 16)
        paginator_construction = Paginator(construction, 16)
        paginator_education = Paginator(education, 16)
        paginator_eldercare = Paginator(eldercare, 16)
        paginator_electronics = Paginator(electronics, 16)
        paginator_entertainment = Paginator(entertainment, 16)
        paginator_farming = Paginator(farming, 16)
        paginator_florists = Paginator(florists, 16)
        paginator_grocery = Paginator(grocery, 16)
        paginator_health = Paginator(health, 16)
        paginator_home = Paginator(home, 16)
        paginator_hotels = Paginator(hotels, 16)
        paginator_jewelry = Paginator(jewelry, 16)
        paginator_legal = Paginator(legal, 16)
        paginator_lifestyle = Paginator(lifestyle, 16)
        paginator_marketing = Paginator(marketing, 16)
        paginator_medical = Paginator(medical, 16)
        paginator_other = Paginator(other, 16)
        paginator_packaging = Paginator(packaging, 16)
        paginator_pets = Paginator(pets, 16)
        paginator_photography = Paginator(photography, 16)
        paginator_professional = Paginator(professional, 16)
        paginator_realestate = Paginator(realestate, 16)
        paginator_recreation = Paginator(recreation, 16)
        paginator_restaurants = Paginator(restaurants, 16)
        paginator_security = Paginator(security, 16)
        paginator_transportation = Paginator(transportation, 16)
        paginator_visual = Paginator(visual, 16)
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-AR':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_ar.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ar.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ar.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ar.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ar.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ar.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ar.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ar.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ar.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ar.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ar.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ar.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ar.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ar.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ar.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ar.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ar.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ar.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ar.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ar.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ar.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ar.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ar.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ar.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ar.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ar.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ar.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ar.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ar.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ar.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ar.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ar.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ar.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ar.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ar.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ar.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ar.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ar.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ar.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ar.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ar.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ar.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ar.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ar.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ar.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ar.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ar.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ar.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ar.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ar.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ar.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ar.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ar.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ar.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ar.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ar.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ar.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ar.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ar.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ar.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ar.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ar.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ar.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ar.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ar.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ar.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ar.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_ar.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-CA':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_ca.objects.all().order_by('category', 'city', 'business_name')),
        beauty = list(vbp_ca.objects.filter(approved=True).filter(category='beauty').order_by('city', 'business_name'))
        books = list(vbp_ca.objects.filter(approved=True).filter(category='books').order_by('city', 'business_name'))
        cars = list(vbp_ca.objects.filter(approved=True).filter(category='cars'))
        child = list(vbp_ca.objects.filter(approved=True).filter(category='child'))
        cleaning = list(vbp_ca.objects.filter(approved=True).filter(category='cleaning'))
        clothing = list(vbp_ca.objects.filter(approved=True).filter(category='clothing'))
        construction = list(vbp_ca.objects.filter(approved=True).filter(category='construction'))
        education = list(vbp_ca.objects.filter(approved=True).filter(category='education'))
        eldercare = list(vbp_ca.objects.filter(approved=True).filter(category='eldercare'))
        electronics = list(vbp_ca.objects.filter(approved=True).filter(category='electronics'))
        entertainment = list(vbp_ca.objects.filter(approved=True).filter(category='entertainment'))
        farming = list(vbp_ca.objects.filter(approved=True).filter(category='farming'))
        florists = list(vbp_ca.objects.filter(approved=True).filter(category='florists'))
        grocery = list(vbp_ca.objects.filter(approved=True).filter(category='grocery'))
        health = list(vbp_ca.objects.filter(approved=True).filter(category='health'))
        home = list(vbp_ca.objects.filter(approved=True).filter(category='home'))
        hotels = list(vbp_ca.objects.filter(approved=True).filter(category='hotels'))
        jewelry = list(vbp_ca.objects.filter(approved=True).filter(category='jewelry'))
        legal = list(vbp_ca.objects.filter(approved=True).filter(category='legal'))
        lifestyle = list(vbp_ca.objects.filter(approved=True).filter(category='lifestyle'))
        marketing = list(vbp_ca.objects.filter(approved=True).filter(category='marketing'))
        medical = list(vbp_ca.objects.filter(approved=True).filter(category='medical'))
        other = list(vbp_ca.objects.filter(approved=True).filter(category='other'))
        packaging = list(vbp_ca.objects.filter(approved=True).filter(category='packaging'))
        pets = list(vbp_ca.objects.filter(approved=True).filter(category='pets'))
        photography = list(vbp_ca.objects.filter(approved=True).filter(category='photography'))
        professional = list(vbp_ca.objects.filter(approved=True).filter(category='professional'))
        realestate = list(vbp_ca.objects.filter(approved=True).filter(category='real estate'))
        recreation = list(vbp_ca.objects.filter(approved=True).filter(category='recreation'))
        restaurants = list(vbp_ca.objects.filter(approved=True).filter(category='restaurants'))
        security = list(vbp_ca.objects.filter(approved=True).filter(category='security'))
        transportation = list(vbp_ca.objects.filter(approved=True).filter(category='transportation'))
        visual = list(vbp_ca.objects.filter(approved=True).filter(category='visual'))

        paginator_beauty = Paginator(beauty, 16)
        paginator_books = Paginator(books, 16)
        paginator_cars = Paginator(cars, 16)
        paginator_child = Paginator(child, 16)
        paginator_cleaning = Paginator(cleaning, 16)
        paginator_clothing = Paginator(clothing, 16)
        paginator_construction = Paginator(construction, 16)
        paginator_education = Paginator(education, 16)
        paginator_eldercare = Paginator(eldercare, 16)
        paginator_electronics = Paginator(electronics, 16)
        paginator_entertainment = Paginator(entertainment, 16)
        paginator_farming = Paginator(farming, 16)
        paginator_florists = Paginator(florists, 16)
        paginator_grocery = Paginator(grocery, 16)
        paginator_health = Paginator(health, 16)
        paginator_home = Paginator(home, 16)
        paginator_hotels = Paginator(hotels, 16)
        paginator_jewelry = Paginator(jewelry, 16)
        paginator_legal = Paginator(legal, 16)
        paginator_lifestyle = Paginator(lifestyle, 16)
        paginator_marketing = Paginator(marketing, 16)
        paginator_medical = Paginator(medical, 16)
        paginator_other = Paginator(other, 16)
        paginator_packaging = Paginator(packaging, 16)
        paginator_pets = Paginator(pets, 16)
        paginator_photography = Paginator(photography, 16)
        paginator_professional = Paginator(professional, 16)
        paginator_realestate = Paginator(realestate, 16)
        paginator_recreation = Paginator(recreation, 16)
        paginator_restaurants = Paginator(restaurants, 16)
        paginator_security = Paginator(security, 16)
        paginator_transportation = Paginator(transportation, 16)
        paginator_visual = Paginator(visual, 16)
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-CO':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_co.objects.all().order_by('category', 'city', 'business_name')),
        beauty = list(vbp_co.objects.filter(approved=True).filter(category='beauty').order_by('city', 'business_name'))
        books = list(vbp_co.objects.filter(approved=True).filter(category='books').order_by('city', 'business_name'))
        cars = list(vbp_co.objects.filter(approved=True).filter(category='cars'))
        child = list(vbp_co.objects.filter(approved=True).filter(category='child'))
        cleaning = list(vbp_co.objects.filter(approved=True).filter(category='cleaning'))
        clothing = list(vbp_co.objects.filter(approved=True).filter(category='clothing'))
        construction = list(vbp_co.objects.filter(approved=True).filter(category='construction'))
        education = list(vbp_co.objects.filter(approved=True).filter(category='education'))
        eldercare = list(vbp_co.objects.filter(approved=True).filter(category='eldercare'))
        electronics = list(vbp_co.objects.filter(approved=True).filter(category='electronics'))
        entertainment = list(vbp_co.objects.filter(approved=True).filter(category='entertainment'))
        farming = list(vbp_co.objects.filter(approved=True).filter(category='farming'))
        florists = list(vbp_co.objects.filter(approved=True).filter(category='florists'))
        grocery = list(vbp_co.objects.filter(approved=True).filter(category='grocery'))
        health = list(vbp_co.objects.filter(approved=True).filter(category='health'))
        home = list(vbp_co.objects.filter(approved=True).filter(category='home'))
        hotels = list(vbp_co.objects.filter(approved=True).filter(category='hotels'))
        jewelry = list(vbp_co.objects.filter(approved=True).filter(category='jewelry'))
        legal = list(vbp_co.objects.filter(approved=True).filter(category='legal'))
        lifestyle = list(vbp_co.objects.filter(approved=True).filter(category='lifestyle'))
        marketing = list(vbp_co.objects.filter(approved=True).filter(category='marketing'))
        medical = list(vbp_co.objects.filter(approved=True).filter(category='medical'))
        other = list(vbp_co.objects.filter(approved=True).filter(category='other'))
        packaging = list(vbp_co.objects.filter(approved=True).filter(category='packaging'))
        pets = list(vbp_co.objects.filter(approved=True).filter(category='pets'))
        photography = list(vbp_co.objects.filter(approved=True).filter(category='photography'))
        professional = list(vbp_co.objects.filter(approved=True).filter(category='professional'))
        realestate = list(vbp_co.objects.filter(approved=True).filter(category='real estate'))
        recreation = list(vbp_co.objects.filter(approved=True).filter(category='recreation'))
        restaurants = list(vbp_co.objects.filter(approved=True).filter(category='restaurants'))
        security = list(vbp_co.objects.filter(approved=True).filter(category='security'))
        transportation = list(vbp_co.objects.filter(approved=True).filter(category='transportation'))
        visual = list(vbp_co.objects.filter(approved=True).filter(category='visual'))

        paginator_beauty = Paginator(beauty, 16)
        paginator_books = Paginator(books, 16)
        paginator_cars = Paginator(cars, 16)
        paginator_child = Paginator(child, 16)
        paginator_cleaning = Paginator(cleaning, 16)
        paginator_clothing = Paginator(clothing, 16)
        paginator_construction = Paginator(construction, 16)
        paginator_education = Paginator(education, 16)
        paginator_eldercare = Paginator(eldercare, 16)
        paginator_electronics = Paginator(electronics, 16)
        paginator_entertainment = Paginator(entertainment, 16)
        paginator_farming = Paginator(farming, 16)
        paginator_florists = Paginator(florists, 16)
        paginator_grocery = Paginator(grocery, 16)
        paginator_health = Paginator(health, 16)
        paginator_home = Paginator(home, 16)
        paginator_hotels = Paginator(hotels, 16)
        paginator_jewelry = Paginator(jewelry, 16)
        paginator_legal = Paginator(legal, 16)
        paginator_lifestyle = Paginator(lifestyle, 16)
        paginator_marketing = Paginator(marketing, 16)
        paginator_medical = Paginator(medical, 16)
        paginator_other = Paginator(other, 16)
        paginator_packaging = Paginator(packaging, 16)
        paginator_pets = Paginator(pets, 16)
        paginator_photography = Paginator(photography, 16)
        paginator_professional = Paginator(professional, 16)
        paginator_realestate = Paginator(realestate, 16)
        paginator_recreation = Paginator(recreation, 16)
        paginator_restaurants = Paginator(restaurants, 16)
        paginator_security = Paginator(security, 16)
        paginator_transportation = Paginator(transportation, 16)
        paginator_visual = Paginator(visual, 16)
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-CT':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_ct.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ct.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ct.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ct.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ct.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ct.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ct.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ct.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ct.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ct.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ct.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ct.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ct.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ct.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ct.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ct.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ct.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ct.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ct.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ct.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ct.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ct.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ct.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ct.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ct.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ct.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ct.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ct.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ct.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ct.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ct.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ct.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ct.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ct.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ct.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ct.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ct.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ct.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ct.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ct.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ct.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ct.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ct.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ct.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ct.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ct.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ct.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ct.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ct.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ct.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ct.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ct.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ct.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ct.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ct.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ct.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ct.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ct.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ct.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ct.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ct.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ct.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ct.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ct.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ct.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ct.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ct.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_ct.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-DE':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_de.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_de.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_de.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_de.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_de.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_de.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_de.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_de.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_de.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_de.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_de.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_de.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_de.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_de.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_de.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_de.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_de.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_de.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_de.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_de.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_de.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_de.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_de.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_de.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_de.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_de.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_de.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_de.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_de.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_de.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_de.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_de.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_de.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_de.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_de.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_de.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_de.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_de.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_de.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_de.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_de.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_de.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_de.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_de.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_de.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_de.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_de.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_de.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_de.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_de.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_de.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_de.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_de.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_de.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_de.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_de.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_de.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_de.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_de.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_de.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_de.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_de.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_de.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_de.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_de.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_de.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_de.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_de.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-DC':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_dc.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_dc.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_dc.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_dc.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_dc.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_dc.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_dc.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_dc.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_dc.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_dc.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_dc.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_dc.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_dc.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_dc.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_dc.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_dc.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_dc.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_dc.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_dc.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_dc.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_dc.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_dc.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_dc.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_dc.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_dc.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_dc.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_dc.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_dc.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_dc.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_dc.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_dc.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_dc.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_dc.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_dc.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_dc.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_dc.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_dc.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_dc.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_dc.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_dc.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_dc.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_dc.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_dc.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_dc.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_dc.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_dc.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_dc.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_dc.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_dc.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_dc.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_dc.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_dc.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_dc.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_dc.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_dc.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_dc.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_dc.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_dc.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_dc.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_dc.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_dc.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_dc.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_dc.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_dc.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_dc.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_dc.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_dc.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_dc.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-FL':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_fl.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_fl.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_fl.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_fl.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_fl.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_fl.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_fl.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_fl.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_fl.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_fl.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_fl.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_fl.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_fl.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_fl.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_fl.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_fl.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_fl.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_fl.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_fl.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_fl.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_fl.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_fl.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_fl.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_fl.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_fl.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_fl.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_fl.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_fl.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_fl.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_fl.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_fl.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_fl.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_fl.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_fl.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_fl.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_fl.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_fl.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_fl.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_fl.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_fl.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_fl.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_fl.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_fl.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_fl.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_fl.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_fl.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_fl.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_fl.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_fl.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_fl.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_fl.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_fl.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_fl.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_fl.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_fl.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_fl.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_fl.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_fl.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_fl.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_fl.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_fl.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_fl.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_fl.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_fl.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_fl.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_fl.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_fl.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_fl.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            ) 
    if state == 'US-GA':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_ga.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ga.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ga.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ga.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ga.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ga.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ga.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ga.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ga.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ga.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ga.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ga.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ga.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ga.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ga.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ga.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ga.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ga.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ga.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ga.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ga.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ga.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ga.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ga.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ga.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ga.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ga.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ga.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ga.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ga.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ga.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ga.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ga.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ga.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ga.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ga.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ga.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ga.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ga.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ga.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ga.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ga.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ga.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ga.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ga.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ga.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ga.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ga.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ga.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ga.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ga.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ga.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ga.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ga.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ga.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ga.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ga.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ga.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ga.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ga.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ga.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ga.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ga.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ga.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ga.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ga.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ga.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_ga.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-HI':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_hi.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_hi.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_hi.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_hi.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_hi.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_hi.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_hi.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_hi.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_hi.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_hi.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_hi.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_hi.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_hi.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_hi.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_hi.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_hi.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_hi.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_hi.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_hi.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_hi.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_hi.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_hi.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_hi.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_hi.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_hi.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_hi.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_hi.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_hi.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_hi.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_hi.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_hi.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_hi.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_hi.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_hi.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_hi.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_hi.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_hi.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_hi.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_hi.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_hi.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_hi.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_hi.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_hi.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_hi.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_hi.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_hi.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_hi.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_hi.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_hi.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_hi.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_hi.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_hi.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_hi.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_hi.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_hi.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_hi.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_hi.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_hi.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_hi.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_hi.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_hi.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_hi.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_hi.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_hi.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_hi.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_hi.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_hi.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_hi.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-ID':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_id.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_id.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_id.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_id.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_id.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_id.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_id.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_id.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_id.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_id.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_id.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_id.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_id.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_id.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_id.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_id.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_id.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_id.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_id.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_id.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_id.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_id.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_id.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_id.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_id.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_id.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_id.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_id.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_id.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_id.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_id.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_id.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_id.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_id.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_id.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_id.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_id.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_id.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_id.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_id.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_id.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_id.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_id.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_id.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_id.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_id.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_id.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_id.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_id.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_id.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_id.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_id.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_id.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_id.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_id.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_id.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_id.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_id.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_id.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_id.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_id.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_id.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_id.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_id.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_id.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_id.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_id.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_id.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-IL':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_il.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_il.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_il.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_il.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_il.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_il.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_il.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_il.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_il.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_il.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_il.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_il.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_il.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_il.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_il.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_il.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_il.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_il.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_il.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_il.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_il.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_il.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_il.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_il.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_il.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_il.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_il.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_il.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_il.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_il.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_il.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_il.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_il.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_il.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_il.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_il.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_il.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_il.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_il.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_il.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_il.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_il.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_il.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_il.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_il.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_il.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_il.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_il.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_il.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_il.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_il.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_il.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_il.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_il.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_il.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_il.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_il.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_il.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_il.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_il.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_il.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_il.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_il.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_il.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_il.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_il.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_il.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_il.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-IN':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_in.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_in.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_in.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_in.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_in.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_in.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_in.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_in.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_in.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_in.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_in.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_in.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_in.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_in.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_in.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_in.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_in.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_in.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_in.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_in.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_in.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_in.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_in.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_in.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_in.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_in.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_in.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_in.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_in.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_in.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_in.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_in.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_in.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_in.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_in.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_in.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_in.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_in.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_in.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_in.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_in.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_in.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_in.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_in.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_in.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_in.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_in.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_in.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_in.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_in.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_in.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_in.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_in.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_in.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_in.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_in.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_in.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_in.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_in.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_in.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_in.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_in.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_in.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_in.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_in.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_in.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_in.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_in.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-IA':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_ia.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ia.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ia.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ia.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ia.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ia.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ia.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ia.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ia.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ia.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ia.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ia.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ia.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ia.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ia.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ia.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ia.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ia.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ia.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ia.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ia.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ia.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ia.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ia.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ia.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ia.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ia.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ia.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ia.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ia.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ia.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ia.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ia.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ia.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ia.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ia.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ia.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ia.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ia.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ia.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ia.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ia.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ia.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ia.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ia.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ia.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ia.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ia.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ia.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ia.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ia.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ia.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ia.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ia.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ia.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ia.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ia.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ia.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ia.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ia.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ia.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ia.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ia.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ia.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ia.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ia.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ia.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_ia.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-KS':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_ks.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ks.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ks.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ks.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ks.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ks.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ks.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ks.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ks.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ks.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ks.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ks.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ks.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ks.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ks.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ks.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ks.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ks.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ks.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ks.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ks.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ks.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ks.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ks.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ks.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ks.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ks.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ks.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ks.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ks.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ks.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ks.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ks.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ks.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ks.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ks.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ks.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ks.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ks.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ks.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ks.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ks.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ks.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ks.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ks.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ks.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ks.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ks.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ks.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ks.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ks.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ks.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ks.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ks.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ks.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ks.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ks.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ks.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ks.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ks.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ks.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ks.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ks.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ks.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ks.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ks.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ks.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_ks.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-KY':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_ky.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-LA':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_la.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_la.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_la.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_la.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_la.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_la.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_la.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_la.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_la.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_la.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_la.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_la.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_la.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_la.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_la.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_la.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_la.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_la.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_la.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_la.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_la.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_la.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_la.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_la.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_la.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_la.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_la.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_la.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_la.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_la.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_la.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_la.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_la.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_la.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_la.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_la.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_la.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_la.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_la.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_la.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_la.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_la.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_la.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_la.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_la.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_la.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_la.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_la.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_la.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_la.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_la.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_la.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_la.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_la.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_la.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_la.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_la.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_la.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_la.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_la.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_la.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_la.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_la.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_la.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_la.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_la.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_la.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_la.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-ME':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_me.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-MD':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_md.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_md.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_md.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_md.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_md.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_md.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_md.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_md.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_md.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_md.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_md.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_md.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_md.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_md.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_md.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_md.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_md.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_md.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_md.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_md.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_md.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_md.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_md.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_md.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_md.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_md.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_md.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_md.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_md.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_md.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_md.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_md.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_md.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_md.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_md.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_md.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_md.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_md.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_md.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_md.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_md.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_md.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_md.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_md.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_md.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_md.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_md.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_md.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_md.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_md.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_md.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_md.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_md.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_md.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_md.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_md.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_md.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_md.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_md.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_md.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_md.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_md.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_md.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_md.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_md.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_md.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_md.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_md.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-MA':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_ma.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ma.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ma.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ma.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ma.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ma.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ma.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ma.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ma.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ma.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ma.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ma.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ma.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ma.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ma.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ma.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ma.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ma.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ma.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ma.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ma.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ma.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ma.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ma.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ma.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ma.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ma.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ma.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ma.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ma.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ma.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ma.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ma.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ma.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ma.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ma.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ma.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ma.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ma.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ma.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ma.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ma.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ma.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ma.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ma.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ma.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ma.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ma.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ma.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ma.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ma.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ma.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ma.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ma.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ma.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ma.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ma.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ma.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ma.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ma.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ma.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ma.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ma.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ma.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ma.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ma.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ma.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_ma.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-MI':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_mi.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_mi.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_mi.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_mi.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_mi.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_mi.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_mi.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_mi.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_mi.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_mi.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_mi.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_mi.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_mi.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_mi.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_mi.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_mi.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_mi.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_mi.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_mi.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_mi.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_mi.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_mi.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_mi.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_mi.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_mi.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_mi.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_mi.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_mi.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_mi.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_mi.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_mi.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_mi.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_mi.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_mi.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_mi.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_mi.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_mi.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_mi.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_mi.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_mi.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_mi.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_mi.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_mi.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_mi.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_mi.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_mi.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_mi.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_mi.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_mi.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_mi.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_mi.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_mi.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_mi.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_mi.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_mi.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_mi.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_mi.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_mi.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_mi.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_mi.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_mi.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_mi.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_mi.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_mi.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_mi.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_mi.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_mi.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_mi.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )  
    if state == 'US-MS':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_ms.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ms.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ms.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ms.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ms.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ms.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ms.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ms.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ms.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ms.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ms.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ms.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ms.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ms.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ms.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ms.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ms.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ms.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ms.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ms.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ms.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ms.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ms.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ms.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ms.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ms.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ms.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ms.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ms.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ms.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ms.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ms.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ms.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ms.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ms.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ms.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ms.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ms.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ms.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ms.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ms.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ms.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ms.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ms.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ms.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ms.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ms.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ms.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ms.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ms.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ms.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ms.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ms.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ms.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ms.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ms.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ms.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ms.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ms.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ms.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ms.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ms.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ms.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ms.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ms.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ms.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ms.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_ms.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-MN':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_mn.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-MO':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_mo.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_mo.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_mo.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_mo.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_mo.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_mo.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_mo.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_mo.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_mo.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_mo.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_mo.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_mo.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_mo.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_mo.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_mo.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_mo.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_mo.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_mo.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_mo.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_mo.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_mo.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_mo.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_mo.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_mo.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_mo.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_mo.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_mo.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_mo.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_mo.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_mo.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_mo.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_mo.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_mo.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_mo.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_mo.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_mo.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_mo.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_mo.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_mo.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_mo.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_mo.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_mo.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_mo.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_mo.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_mo.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_mo.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_mo.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_mo.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_mo.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_mo.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_mo.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_mo.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_mo.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_mo.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_mo.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_mo.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_mo.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_mo.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_mo.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_mo.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_mo.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_mo.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_mo.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_mo.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_mo.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_mo.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_mo.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_mo.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-MT':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_mt.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-NE':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_ne.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-NV':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_nv.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-NH':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_nh.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-NJ':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_nj.objects.all(),
        beauty_full = vbp_nj.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_nj.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_nj.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_nj.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_nj.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_nj.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_nj.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_nj.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_nj.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_nj.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_nj.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_nj.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_nj.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_nj.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_nj.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_nj.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_nj.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_nj.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_nj.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_nj.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_nj.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_nj.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_nj.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_nj.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_nj.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_nj.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_nj.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_nj.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_nj.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_nj.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_nj.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_nj.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_nj.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_nj.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_nj.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_nj.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_nj.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_nj.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_nj.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_nj.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_nj.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_nj.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_nj.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_nj.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_nj.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_nj.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_nj.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_nj.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_nj.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_nj.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_nj.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_nj.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_nj.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_nj.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_nj.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_nj.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_nj.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_nj.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_nj.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_nj.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_nj.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_nj.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_nj.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_nj.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_nj.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_nj.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_nj.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-NM':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_nm.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-NY':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_ny.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ny.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ny.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ny.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ny.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ny.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ny.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ny.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ny.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ny.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ny.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ny.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ny.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ny.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ny.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ny.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ny.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ny.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ny.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ny.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ny.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ny.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ny.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ny.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ny.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ny.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ny.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ny.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ny.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ny.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ny.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ny.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ny.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ny.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ny.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ny.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ny.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ny.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ny.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ny.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ny.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ny.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ny.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ny.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ny.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ny.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ny.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ny.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ny.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ny.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ny.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ny.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ny.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ny.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ny.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ny.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ny.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ny.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ny.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ny.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ny.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ny.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ny.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ny.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ny.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ny.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ny.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_ny.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-NC':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_nc.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-ND':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_nd.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-OH':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_oh.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_oh.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_oh.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_oh.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_oh.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_oh.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_oh.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_oh.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_oh.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_oh.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_oh.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_oh.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_oh.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_oh.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_oh.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_oh.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_oh.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_oh.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_oh.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_oh.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_oh.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_oh.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_oh.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_oh.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_oh.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_oh.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_oh.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_oh.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_oh.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_oh.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_oh.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_oh.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_oh.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_oh.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_oh.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_oh.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_oh.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_oh.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_oh.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_oh.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_oh.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_oh.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_oh.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_oh.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_oh.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_oh.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_oh.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_oh.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_oh.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_oh.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_oh.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_oh.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_oh.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_oh.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_oh.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_oh.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_oh.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_oh.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_oh.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_oh.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_oh.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_oh.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_oh.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_oh.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_oh.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_oh.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_oh.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_oh.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-OK':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_ok.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-OR':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_or.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-PA':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_pa.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_pa.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_pa.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_pa.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_pa.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_pa.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_pa.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_pa.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_pa.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_pa.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_pa.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_pa.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_pa.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_pa.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_pa.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_pa.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_pa.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_pa.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_pa.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_pa.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_pa.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_pa.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_pa.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_pa.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_pa.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_pa.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_pa.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_pa.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_pa.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_pa.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_pa.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_pa.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_pa.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_pa.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_pa.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_pa.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_pa.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_pa.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_pa.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_pa.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_pa.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_pa.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_pa.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_pa.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_pa.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_pa.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_pa.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_pa.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_pa.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_pa.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_pa.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_pa.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_pa.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_pa.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_pa.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_pa.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_pa.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_pa.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_pa.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_pa.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_pa.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_pa.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_pa.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_pa.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_pa.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_pa.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_pa.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_pa.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-RI':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_ri.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-SC':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_sc.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_sc.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_sc.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_sc.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_sc.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_sc.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_sc.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_sc.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_sc.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_sc.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_sc.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_sc.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_sc.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_sc.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_sc.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_sc.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_sc.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_sc.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_sc.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_sc.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_sc.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_sc.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_sc.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_sc.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_sc.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_sc.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_sc.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_sc.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_sc.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_sc.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_sc.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_sc.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_sc.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_sc.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_sc.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_sc.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_sc.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_sc.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_sc.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_sc.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_sc.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_sc.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_sc.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_sc.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_sc.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_sc.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_sc.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_sc.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_sc.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_sc.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_sc.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_sc.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_sc.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_sc.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_sc.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_sc.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_sc.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_sc.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_sc.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_sc.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_sc.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_sc.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_sc.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_sc.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_sc.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_sc.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_sc.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_sc.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-SD':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_sd.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-TN':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_tn.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_tn.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_tn.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_tn.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_tn.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_tn.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_tn.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_tn.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_tn.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_tn.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_tn.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_tn.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_tn.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_tn.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_tn.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_tn.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_tn.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_tn.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_tn.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_tn.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_tn.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_tn.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_tn.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_tn.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_tn.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_tn.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_tn.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_tn.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_tn.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_tn.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_tn.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_tn.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_tn.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_tn.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_tn.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_tn.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_tn.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_tn.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_tn.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_tn.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_tn.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_tn.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_tn.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_tn.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_tn.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_tn.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_tn.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_tn.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_tn.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_tn.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_tn.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_tn.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_tn.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_tn.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_tn.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_tn.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_tn.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_tn.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_tn.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_tn.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_tn.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_tn.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_tn.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_tn.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_tn.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_tn.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_tn.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_tn.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-TX':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_tx.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-UT':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_ut.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-VT':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_vt.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-VA':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = list(vbp_va.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_va.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_va.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_va.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_va.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_va.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_va.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_va.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_va.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_va.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_va.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_va.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_va.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_va.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_va.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_va.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_va.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_va.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_va.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_va.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_va.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_va.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_va.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_va.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_va.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_va.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_va.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_va.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_va.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_va.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_va.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_va.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_va.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_va.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_va.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_va.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_va.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_va.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_va.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_va.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_va.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_va.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_va.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_va.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_va.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_va.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_va.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_va.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_va.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_va.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_va.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_va.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_va.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_va.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_va.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_va.objects.filter(approved=True).filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_va.objects.filter(approved=True).filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_va.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_va.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_va.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_va.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_va.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_va.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_va.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_va.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_va.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_va.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
        visual = list(visual_full) + list(visual_blank)

        paginator_beauty = Paginator(beauty, 16)
        beauty_page = 6
        paginator_books = Paginator(books, 16)
        books_page = beauty_page + paginator_beauty.num_pages + 1
        paginator_cars = Paginator(cars, 16)
        cars_page = books_page + paginator_books.num_pages + 1
        paginator_child = Paginator(child, 16)
        child_page = cars_page + paginator_cars.num_pages + 1
        paginator_cleaning = Paginator(cleaning, 16)
        cleaning_page = child_page + paginator_child.num_pages + 1
        paginator_clothing = Paginator(clothing, 16)
        clothing_page = cleaning_page + paginator_cleaning.num_pages + 1
        paginator_construction = Paginator(construction, 16)
        construction_page = clothing_page + paginator_clothing.num_pages + 1
        paginator_education = Paginator(education, 16)
        education_page = construction_page + paginator_construction.num_pages + 1
        paginator_eldercare = Paginator(eldercare, 16)
        eldercare_page = education_page + paginator_education.num_pages + 1
        paginator_electronics = Paginator(electronics, 16)
        electronics_page = eldercare_page + paginator_eldercare.num_pages + 1
        paginator_entertainment = Paginator(entertainment, 16)
        entertainment_page = electronics_page + paginator_electronics.num_pages + 1
        paginator_farming = Paginator(farming, 16)
        farming_page = entertainment_page + paginator_entertainment.num_pages + 1
        paginator_florists = Paginator(florists, 16)
        florists_page = farming_page + paginator_farming.num_pages + 1
        paginator_grocery = Paginator(grocery, 16)
        grocery_page = florists_page + paginator_florists.num_pages + 1
        paginator_health = Paginator(health, 16)
        health_page = grocery_page + paginator_grocery.num_pages + 1
        paginator_home = Paginator(home, 16)
        home_page = health_page + paginator_health.num_pages + 1
        paginator_hotels = Paginator(hotels, 16)
        hotels_page = home_page + paginator_home.num_pages + 1
        paginator_jewelry = Paginator(jewelry, 16)
        jewelry_page = hotels_page + paginator_hotels.num_pages + 1
        paginator_legal = Paginator(legal, 16)
        legal_page = jewelry_page + paginator_jewelry.num_pages + 1
        paginator_lifestyle = Paginator(lifestyle, 16)
        lifestyle_page = legal_page + paginator_legal.num_pages + 1
        paginator_marketing = Paginator(marketing, 16)
        marketing_page = lifestyle_page + paginator_lifestyle.num_pages + 1
        paginator_medical = Paginator(medical, 16)
        medical_page = marketing_page + paginator_marketing.num_pages + 1
        paginator_packaging = Paginator(packaging, 16)
        packaging_page = medical_page + paginator_medical.num_pages + 1
        paginator_pets = Paginator(pets, 16)
        pets_page = packaging_page + paginator_packaging.num_pages + 1
        paginator_photography = Paginator(photography, 16)
        photography_page = pets_page + paginator_pets.num_pages + 1
        paginator_professional = Paginator(professional, 16)
        professional_page = photography_page + paginator_photography.num_pages + 1
        paginator_realestate = Paginator(realestate, 16)
        realestate_page = professional_page + paginator_professional.num_pages + 1
        paginator_recreation = Paginator(recreation, 16)
        recreation_page = realestate_page + paginator_realestate.num_pages + 1
        paginator_restaurants = Paginator(restaurants, 16)
        restaurants_page = recreation_page + paginator_recreation.num_pages + 1
        paginator_security = Paginator(security, 16)
        security_page = restaurants_page + paginator_restaurants.num_pages + 1
        paginator_transportation = Paginator(transportation, 16)
        transportation_page = security_page + paginator_security.num_pages + 1
        paginator_visual = Paginator(visual, 16)
        visual_page = transportation_page + paginator_transportation.num_pages + 1
        paginator_other = Paginator(other, 16)
        other_page = visual_page + paginator_visual.num_pages + 1
        f = StateFilter(request.GET, queryset=vbp_va.objects.all())
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'beauty_page': beauty_page,
            'books_page': books_page,
            'cars_page': cars_page,
            'child_page': child_page,
            'cleaning_page': cleaning_page,
            'clothing_page': clothing_page,
            'construction_page': construction_page,
            'education_page': education_page,
            'eldercare_page': eldercare_page,
            'electronics_page': electronics_page,
            'entertainment_page': entertainment_page,
            'farming_page': farming_page,
            'florists_page': florists_page,
            'grocery_page': grocery_page,
            'health_page': health_page,
            'home_page': home_page,
            'hotels_page': hotels_page,
            'jewelry_page': jewelry_page,
            'legal_page': legal_page,
            'lifestyle_page': lifestyle_page,
            'marketing_page': marketing_page,
            'medical_page': medical_page,
            'packaging_page': packaging_page,
            'pets_page': pets_page,
            'photography_page': photography_page,
            'professional_page': professional_page,
            'realestate_page': realestate_page,
            'recreation_page': recreation_page,
            'restaurants_page': restaurants_page,
            'security_page': security_page,
            'transportation_page': transportation_page,
            'visual_page': visual_page,
            'other_page': other_page,
            'filter': f,
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'beauty': beauty,
            'paginator': paginator,
            'paginator_beauty': paginator_beauty,
            'paginator_books': paginator_books,
            'paginator_cars': paginator_cars,
            'paginator_child': paginator_child,
            'paginator_cleaning': paginator_cleaning,
            'paginator_clothing': paginator_clothing,
            'paginator_construction': paginator_construction,
            'paginator_education': paginator_education,
            'paginator_eldercare': paginator_eldercare,
            'paginator_electronics': paginator_electronics,
            'paginator_entertainment': paginator_entertainment,
            'paginator_farming': paginator_farming,
            'paginator_florists': paginator_florists,
            'paginator_grocery': paginator_grocery,
            'paginator_health': paginator_health,
            'paginator_home': paginator_home,
            'paginator_hotels': paginator_hotels,
            'paginator_jewelry': paginator_jewelry,
            'paginator_legal': paginator_legal,
            'paginator_lifestyle': paginator_lifestyle,
            'paginator_marketing': paginator_marketing,
            'paginator_medical': paginator_medical,
            'paginator_other': paginator_other,
            'paginator_packaging': paginator_packaging,
            'paginator_pets': paginator_pets,
            'paginator_photography': paginator_photography,
            'paginator_professional': paginator_professional,
            'paginator_realestate': paginator_realestate,
            'paginator_recreation': paginator_recreation,
            'paginator_restaurants': paginator_restaurants,
            'paginator_security': paginator_security,
            'paginator_transportation': paginator_transportation,
            'paginator_visual': paginator_visual,
            }
            )
    if state == 'US-WA':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_wa.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-WV':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_wv.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-WI':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_wi.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
    if state == 'US-WY':
        covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
        state_qs = vbp_wy.objects.all().order_by('category', 'city', 'business_name'),
        for object in state_qs:
            obj = list(object)
            paginator = Paginator(obj, 16)
        return render(request, 
            'flipbook.html', 
            {
            'covers_qs': covers_qs,
            'state_qs': state_qs,
            'obj': obj,
            'paginator': paginator,
            }
            )
        
def filterList(request):
    get = request.GET
    
    print(get)
    items = get.items()
    print(items)
    return HttpResponse(220)