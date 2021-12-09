import django
from django.db.models import query, F
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
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
    "barber", "bathandbody", "beautysalon", "beautysupply", "cosmetics", "nails", "travelingstylist", "other"
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
    print(request.GET)
    category = request.GET['category']
    print(category)
    qs = None
    if category == 'beauty':
        qs = BEAUTY_CHOICES
    elif category == 'books':
        qs = BOOK_CHOICES
    elif category == "cars":
        qs = CARS_CHOICES
    elif category == 'child':
        qs = CHILD_CHOICES
    elif category == "cleaning":
        qs = CLEANING_CHOICES
    print(qs)
    return HttpResponse(qs)

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

def ct_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_ct.objects.order_by('city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(category='visual').order_by('city', 'business_name')

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
        

def ny_list(request):
    data = request.GET
    f = StateFilter(data, queryset=vbp_ny.objects.all())
    filtered_qs = f.qs
    beauty = filtered_qs.filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(category='visual').order_by('city', 'business_name')

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
    beauty = filtered_qs.filter(category='beauty').order_by('business_name')
    books = filtered_qs.filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(category='visual').order_by('city', 'business_name')

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
    beauty = filtered_qs.filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(category='visual').order_by('city', 'business_name')

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
    beauty = filtered_qs.filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(category='visual').order_by('city', 'business_name')

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
    beauty = filtered_qs.filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(category='visual').order_by('city', 'business_name')

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
    beauty = filtered_qs.filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(category='visual').order_by('city', 'business_name')

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
    beauty = filtered_qs.filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(category='visual').order_by('city', 'business_name')

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
    beauty = filtered_qs.filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(category='visual').order_by('city', 'business_name')

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
    beauty = filtered_qs.filter(category='beauty').order_by('city', 'business_name')
    books = filtered_qs.filter(category='books').order_by('city', 'business_name')
    cars = filtered_qs.filter(category='cars').order_by('city', 'business_name')
    child = filtered_qs.filter(category='child').order_by('city', 'business_name')
    cleaning = filtered_qs.filter(category='cleaning').order_by('city', 'business_name')
    clothing = filtered_qs.filter(category='clothing').order_by('city', 'business_name')
    construction = filtered_qs.filter(category='construction').order_by('city', 'business_name')
    education = filtered_qs.filter(category='education').order_by('city', 'business_name')
    eldercare = filtered_qs.filter(category='eldercare').order_by('city', 'business_name')
    electronics = filtered_qs.filter(category='electronics').order_by('city', 'business_name')
    entertainment = filtered_qs.filter(category='entertainment').order_by('city', 'business_name')
    farming = filtered_qs.filter(category='farming').order_by('city', 'business_name')
    florists = filtered_qs.filter(category='florists').order_by('city', 'business_name')
    grocery = filtered_qs.filter(category='grocery').order_by('city', 'business_name')
    health = filtered_qs.filter(category='health').order_by('city', 'business_name')
    home = filtered_qs.filter(category='home').order_by('city', 'business_name')
    hotels = filtered_qs.filter(category='hotels').order_by('city', 'business_name')
    jewelry = filtered_qs.filter(category='jewelry').order_by('city', 'business_name')
    legal = filtered_qs.filter(category='legal').order_by('city', 'business_name')
    lifestyle = filtered_qs.filter(category='lifestyle').order_by('city', 'business_name')
    marketing = filtered_qs.filter(category='marketing').order_by('city', 'business_name')
    medical = filtered_qs.filter(category='medical').order_by('city', 'business_name')
    other = filtered_qs.filter(category='other').order_by('city', 'business_name')
    packaging = filtered_qs.filter(category='packaging').order_by('city', 'business_name')
    pets = filtered_qs.filter(category='pets').order_by('city', 'business_name')
    photography = filtered_qs.filter(category='photography').order_by('city', 'business_name')
    professional = filtered_qs.filter(category='professional').order_by('city', 'business_name')
    realestate = filtered_qs.filter(category='real estate').order_by('city', 'business_name')
    recreation = filtered_qs.filter(category='recreation').order_by('city', 'business_name')
    restaurants = filtered_qs.filter(category='restaurants').order_by('city', 'business_name')
    security = filtered_qs.filter(category='security').order_by('city', 'business_name')
    transportation = filtered_qs.filter(category='transportation').order_by('city', 'business_name')
    visual = filtered_qs.filter(category='visual').order_by('city', 'business_name')

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
            category_set = city_set.objects.filter(category=category)
            print(category_set)
    return HttpResponse('success')

def home(request):
    f = StateFilter(request.GET, queryset=vbp_nj.objects.all())
    covers_qs = vbp_book.objects.all()
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
    if request.method == 'POST':
        nomination_form = NominationForm(request.POST)
        if nomination_form.data['state'] == 'AL':
            obj = vbp_al()
        elif nomination_form.data['state'] == 'AZ':
            obj = vbp_az()
        elif nomination_form.data['state'] == 'AR':
            obj = vbp_ar()
        elif nomination_form.data['state'] == 'CA':
            obj = vbp_ca()
        elif nomination_form.data['state'] == 'CO':
            obj = vbp_co()
        elif nomination_form.data['state'] == 'CT':
            obj = vbp_ct()
        elif nomination_form.data['state'] == 'DE':
            obj = vbp_de()
        elif nomination_form.data['state'] == 'DC':
            obj = vbp_dc()
        elif nomination_form.data['state'] == 'FL':
            obj = vbp_fl()
        elif nomination_form.data['state'] == 'GA':
            obj = vbp_ga()
        elif nomination_form.data['state'] == 'HI':
            obj = vbp_hi()
        elif nomination_form.data['state'] == 'ID':
            obj = vbp_id()
        elif nomination_form.data['state'] == 'IL':
            obj = vbp_il()
        elif nomination_form.data['state'] == 'IN':
            obj = vbp_in()
        elif nomination_form.data['state'] == 'IA':
            obj = vbp_ia()
        elif nomination_form.data['state'] == 'KS':
            obj = vbp_ks()
        elif nomination_form.data['state'] == 'KY':
            obj = vbp_ky()
        elif nomination_form.data['state'] == 'LA':
            obj = vbp_la()
        elif nomination_form.data['state'] == 'ME':
            obj = vbp_me()
        elif nomination_form.data['state'] == 'MD':
            obj = vbp_md()
        elif nomination_form.data['state'] == 'MA':
            obj = vbp_ma()
        elif nomination_form.data['state'] == 'MI':
            obj = vbp_mi()
        elif nomination_form.data['state'] == 'MN':
            obj = vbp_mn()
        elif nomination_form.data['state'] == 'MS':
            obj = vbp_ms()
        elif nomination_form.data['state'] == 'MO':
            obj = vbp_mo()
        elif nomination_form.data['state'] == 'MT':
            obj = vbp_mt()
        elif nomination_form.data['state'] == 'NE':
            obj = vbp_ne()
        elif nomination_form.data['state'] == 'NV':
            obj = vbp_nv()
        elif nomination_form.data['state'] == 'NH':
            obj = vbp_nh()
        elif nomination_form.data['state'] == 'NJ':
            obj = vbp_nj()
        elif nomination_form.data['state'] == 'NM':
            obj = vbp_nm()
        elif nomination_form.data['state'] == 'NY':
            obj = vbp_ny()
        elif nomination_form.data['state'] == 'NC':
            obj = vbp_nc()
        elif nomination_form.data['state'] == 'ND':
            obj = vbp_nd()
        elif nomination_form.data['state'] == 'OH':
            obj = vbp_oh()
        elif nomination_form.data['state'] == 'OK':
            obj = vbp_ok()
        elif nomination_form.data['state'] == 'OR':
            obj = vbp_or()
        elif nomination_form.data['state'] == 'PA':
            obj = vbp_pa()
        elif nomination_form.data['state'] == 'RI':
            obj = vbp_ri()
        elif nomination_form.data['state'] == 'SC':
            obj = vbp_sc()
        elif nomination_form.data['state'] == 'SD':
            obj = vbp_sd()
        elif nomination_form.data['state'] == 'TN':
            obj = vbp_tn()
        elif nomination_form.data['state'] == 'TX':
            obj = vbp_tx()
        elif nomination_form.data['state'] == 'UT':
            obj = vbp_ut()
        elif nomination_form.data['state'] == 'VT':
            obj = vbp_vt()
        elif nomination_form.data['state'] == 'VA':
            obj = vbp_va()
        elif nomination_form.data['state'] == 'WA':
            obj = vbp_wa()
        elif nomination_form.data['state'] == 'WV':
            obj = vbp_wv()
        elif nomination_form.data['state'] == 'WI':
            obj = vbp_wi()
        elif nomination_form.data['state'] == 'WY':
            obj = vbp_wy()
        obj.business_name = nomination_form.data['business_name']
        obj.website = nomination_form.data['website']
        obj.city = nomination_form.data['city']
        obj.county = nomination_form.data['county']
        obj.phone = nomination_form.data['phone']
        obj.category = nomination_form.data['category']
        obj.subcategory = nomination_form.data['subcategory']
        obj.approved = 'False'
        if request.user.is_authenticated:
            obj.user = request.user
            obj.team = request.user.team
            obj.nominator_email = request.user.email
            obj.nominator_name = request.user.full_name
        else:
            obj.nominator_email = nomination_form.data['nominator_email']
            obj.nominator_name = nomination_form.data['nominator_name']
        obj.save()
        sweetify.success(request, title='Thank you!', icon='success', text='Thank you for nominating a Black-owned business!', button='Nominate Another Business', timer=4000)
        
        return redirect('/black-friday-challenge')
    else:
        nomination_form = NominationForm()
    return render(
        request, 
        'vbp_list.html', 
        {
        'covers_qs': covers_qs,
        'title': 'ETV | Village Black Pages',
        'initial_qs': initial_qs,
        'nomination_form': nomination_form,
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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_al.objects.all().order_by('city', 'business_name')),
        beauty = list(vbp_al.objects.filter(category='beauty').order_by('city', 'business_name'))
        books = list(vbp_al.objects.filter(category='books').order_by('city', 'business_name'))
        cars = list(vbp_al.objects.filter(category='cars'))
        child = list(vbp_al.objects.filter(category='child'))
        cleaning = list(vbp_al.objects.filter(category='cleaning'))
        clothing = list(vbp_al.objects.filter(category='clothing'))
        construction = list(vbp_al.objects.filter(category='construction'))
        education = list(vbp_al.objects.filter(category='education'))
        eldercare = list(vbp_al.objects.filter(category='eldercare'))
        electronics = list(vbp_al.objects.filter(category='electronics'))
        entertainment = list(vbp_al.objects.filter(category='entertainment'))
        farming = list(vbp_al.objects.filter(category='farming'))
        florists = list(vbp_al.objects.filter(category='florists'))
        grocery = list(vbp_al.objects.filter(category='grocery'))
        health = list(vbp_al.objects.filter(category='health'))
        home = list(vbp_al.objects.filter(category='home'))
        hotels = list(vbp_al.objects.filter(category='hotels'))
        jewelry = list(vbp_al.objects.filter(category='jewelry'))
        legal = list(vbp_al.objects.filter(category='legal'))
        lifestyle = list(vbp_al.objects.filter(category='lifestyle'))
        marketing = list(vbp_al.objects.filter(category='marketing'))
        medical = list(vbp_al.objects.filter(category='medical'))
        other = list(vbp_al.objects.filter(category='other'))
        packaging = list(vbp_al.objects.filter(category='packaging'))
        pets = list(vbp_al.objects.filter(category='pets'))
        photography = list(vbp_al.objects.filter(category='photography'))
        professional = list(vbp_al.objects.filter(category='professional'))
        realestate = list(vbp_al.objects.filter(category='real estate'))
        recreation = list(vbp_al.objects.filter(category='recreation'))
        restaurants = list(vbp_al.objects.filter(category='restaurants'))
        security = list(vbp_al.objects.filter(category='security'))
        transportation = list(vbp_al.objects.filter(category='transportation'))
        visual = list(vbp_al.objects.filter(category='visual'))

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
    if state == 'US-AZ':
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_az.objects.all().order_by('category', 'city', 'business_name')),
        beauty = list(vbp_az.objects.filter(category='beauty').order_by('city', 'business_name'))
        books = list(vbp_az.objects.filter(category='books').order_by('city', 'business_name'))
        cars = list(vbp_az.objects.filter(category='cars'))
        child = list(vbp_az.objects.filter(category='child'))
        cleaning = list(vbp_az.objects.filter(category='cleaning'))
        clothing = list(vbp_az.objects.filter(category='clothing'))
        construction = list(vbp_az.objects.filter(category='construction'))
        education = list(vbp_az.objects.filter(category='education'))
        eldercare = list(vbp_az.objects.filter(category='eldercare'))
        electronics = list(vbp_az.objects.filter(category='electronics'))
        entertainment = list(vbp_az.objects.filter(category='entertainment'))
        farming = list(vbp_az.objects.filter(category='farming'))
        florists = list(vbp_az.objects.filter(category='florists'))
        grocery = list(vbp_az.objects.filter(category='grocery'))
        health = list(vbp_az.objects.filter(category='health'))
        home = list(vbp_az.objects.filter(category='home'))
        hotels = list(vbp_az.objects.filter(category='hotels'))
        jewelry = list(vbp_az.objects.filter(category='jewelry'))
        legal = list(vbp_az.objects.filter(category='legal'))
        lifestyle = list(vbp_az.objects.filter(category='lifestyle'))
        marketing = list(vbp_az.objects.filter(category='marketing'))
        medical = list(vbp_az.objects.filter(category='medical'))
        other = list(vbp_az.objects.filter(category='other'))
        packaging = list(vbp_az.objects.filter(category='packaging'))
        pets = list(vbp_az.objects.filter(category='pets'))
        photography = list(vbp_az.objects.filter(category='photography'))
        professional = list(vbp_az.objects.filter(category='professional'))
        realestate = list(vbp_az.objects.filter(category='real estate'))
        recreation = list(vbp_az.objects.filter(category='recreation'))
        restaurants = list(vbp_az.objects.filter(category='restaurants'))
        security = list(vbp_az.objects.filter(category='security'))
        transportation = list(vbp_az.objects.filter(category='transportation'))
        visual = list(vbp_az.objects.filter(category='visual'))

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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_ar.objects.all().order_by('category', 'city', 'business_name')),
        beauty = list(vbp_ar.objects.filter(category='beauty').order_by('city', 'business_name'))
        books = list(vbp_ar.objects.filter(category='books').order_by('city', 'business_name'))
        cars = list(vbp_ar.objects.filter(category='cars'))
        child = list(vbp_ar.objects.filter(category='child'))
        cleaning = list(vbp_ar.objects.filter(category='cleaning'))
        clothing = list(vbp_ar.objects.filter(category='clothing'))
        construction = list(vbp_ar.objects.filter(category='construction'))
        education = list(vbp_ar.objects.filter(category='education'))
        eldercare = list(vbp_ar.objects.filter(category='eldercare'))
        electronics = list(vbp_ar.objects.filter(category='electronics'))
        entertainment = list(vbp_ar.objects.filter(category='entertainment'))
        farming = list(vbp_ar.objects.filter(category='farming'))
        florists = list(vbp_ar.objects.filter(category='florists'))
        grocery = list(vbp_ar.objects.filter(category='grocery'))
        health = list(vbp_ar.objects.filter(category='health'))
        home = list(vbp_ar.objects.filter(category='home'))
        hotels = list(vbp_ar.objects.filter(category='hotels'))
        jewelry = list(vbp_ar.objects.filter(category='jewelry'))
        legal = list(vbp_ar.objects.filter(category='legal'))
        lifestyle = list(vbp_ar.objects.filter(category='lifestyle'))
        marketing = list(vbp_ar.objects.filter(category='marketing'))
        medical = list(vbp_ar.objects.filter(category='medical'))
        other = list(vbp_ar.objects.filter(category='other'))
        packaging = list(vbp_ar.objects.filter(category='packaging'))
        pets = list(vbp_ar.objects.filter(category='pets'))
        photography = list(vbp_ar.objects.filter(category='photography'))
        professional = list(vbp_ar.objects.filter(category='professional'))
        realestate = list(vbp_ar.objects.filter(category='real estate'))
        recreation = list(vbp_ar.objects.filter(category='recreation'))
        restaurants = list(vbp_ar.objects.filter(category='restaurants'))
        security = list(vbp_ar.objects.filter(category='security'))
        transportation = list(vbp_ar.objects.filter(category='transportation'))
        visual = list(vbp_ar.objects.filter(category='visual'))

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
    if state == 'US-CA':
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_ca.objects.all().order_by('category', 'city', 'business_name')),
        beauty = list(vbp_ca.objects.filter(category='beauty').order_by('city', 'business_name'))
        books = list(vbp_ca.objects.filter(category='books').order_by('city', 'business_name'))
        cars = list(vbp_ca.objects.filter(category='cars'))
        child = list(vbp_ca.objects.filter(category='child'))
        cleaning = list(vbp_ca.objects.filter(category='cleaning'))
        clothing = list(vbp_ca.objects.filter(category='clothing'))
        construction = list(vbp_ca.objects.filter(category='construction'))
        education = list(vbp_ca.objects.filter(category='education'))
        eldercare = list(vbp_ca.objects.filter(category='eldercare'))
        electronics = list(vbp_ca.objects.filter(category='electronics'))
        entertainment = list(vbp_ca.objects.filter(category='entertainment'))
        farming = list(vbp_ca.objects.filter(category='farming'))
        florists = list(vbp_ca.objects.filter(category='florists'))
        grocery = list(vbp_ca.objects.filter(category='grocery'))
        health = list(vbp_ca.objects.filter(category='health'))
        home = list(vbp_ca.objects.filter(category='home'))
        hotels = list(vbp_ca.objects.filter(category='hotels'))
        jewelry = list(vbp_ca.objects.filter(category='jewelry'))
        legal = list(vbp_ca.objects.filter(category='legal'))
        lifestyle = list(vbp_ca.objects.filter(category='lifestyle'))
        marketing = list(vbp_ca.objects.filter(category='marketing'))
        medical = list(vbp_ca.objects.filter(category='medical'))
        other = list(vbp_ca.objects.filter(category='other'))
        packaging = list(vbp_ca.objects.filter(category='packaging'))
        pets = list(vbp_ca.objects.filter(category='pets'))
        photography = list(vbp_ca.objects.filter(category='photography'))
        professional = list(vbp_ca.objects.filter(category='professional'))
        realestate = list(vbp_ca.objects.filter(category='real estate'))
        recreation = list(vbp_ca.objects.filter(category='recreation'))
        restaurants = list(vbp_ca.objects.filter(category='restaurants'))
        security = list(vbp_ca.objects.filter(category='security'))
        transportation = list(vbp_ca.objects.filter(category='transportation'))
        visual = list(vbp_ca.objects.filter(category='visual'))

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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_co.objects.all().order_by('category', 'city', 'business_name')),
        beauty = list(vbp_co.objects.filter(category='beauty').order_by('city', 'business_name'))
        books = list(vbp_co.objects.filter(category='books').order_by('city', 'business_name'))
        cars = list(vbp_co.objects.filter(category='cars'))
        child = list(vbp_co.objects.filter(category='child'))
        cleaning = list(vbp_co.objects.filter(category='cleaning'))
        clothing = list(vbp_co.objects.filter(category='clothing'))
        construction = list(vbp_co.objects.filter(category='construction'))
        education = list(vbp_co.objects.filter(category='education'))
        eldercare = list(vbp_co.objects.filter(category='eldercare'))
        electronics = list(vbp_co.objects.filter(category='electronics'))
        entertainment = list(vbp_co.objects.filter(category='entertainment'))
        farming = list(vbp_co.objects.filter(category='farming'))
        florists = list(vbp_co.objects.filter(category='florists'))
        grocery = list(vbp_co.objects.filter(category='grocery'))
        health = list(vbp_co.objects.filter(category='health'))
        home = list(vbp_co.objects.filter(category='home'))
        hotels = list(vbp_co.objects.filter(category='hotels'))
        jewelry = list(vbp_co.objects.filter(category='jewelry'))
        legal = list(vbp_co.objects.filter(category='legal'))
        lifestyle = list(vbp_co.objects.filter(category='lifestyle'))
        marketing = list(vbp_co.objects.filter(category='marketing'))
        medical = list(vbp_co.objects.filter(category='medical'))
        other = list(vbp_co.objects.filter(category='other'))
        packaging = list(vbp_co.objects.filter(category='packaging'))
        pets = list(vbp_co.objects.filter(category='pets'))
        photography = list(vbp_co.objects.filter(category='photography'))
        professional = list(vbp_co.objects.filter(category='professional'))
        realestate = list(vbp_co.objects.filter(category='real estate'))
        recreation = list(vbp_co.objects.filter(category='recreation'))
        restaurants = list(vbp_co.objects.filter(category='restaurants'))
        security = list(vbp_co.objects.filter(category='security'))
        transportation = list(vbp_co.objects.filter(category='transportation'))
        visual = list(vbp_co.objects.filter(category='visual'))

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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_ct.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ct.objects.filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ct.objects.filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ct.objects.filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ct.objects.filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ct.objects.filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ct.objects.filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ct.objects.filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ct.objects.filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ct.objects.filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ct.objects.filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ct.objects.filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ct.objects.filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ct.objects.filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ct.objects.filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ct.objects.filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ct.objects.filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ct.objects.filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ct.objects.filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ct.objects.filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ct.objects.filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ct.objects.filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ct.objects.filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ct.objects.filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ct.objects.filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ct.objects.filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ct.objects.filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ct.objects.filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ct.objects.filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ct.objects.filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ct.objects.filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ct.objects.filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ct.objects.filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ct.objects.filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ct.objects.filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ct.objects.filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ct.objects.filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ct.objects.filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ct.objects.filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ct.objects.filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ct.objects.filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ct.objects.filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ct.objects.filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ct.objects.filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ct.objects.filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ct.objects.filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ct.objects.filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ct.objects.filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ct.objects.filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ct.objects.filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ct.objects.filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ct.objects.filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ct.objects.filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ct.objects.filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ct.objects.filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ct.objects.filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ct.objects.filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ct.objects.filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ct.objects.filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ct.objects.filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ct.objects.filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ct.objects.filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ct.objects.filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ct.objects.filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ct.objects.filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ct.objects.filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ct.objects.filter(category='visual').filter(city='').order_by('business_name')
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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_de.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_de.objects.filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_de.objects.filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_de.objects.filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_de.objects.filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_de.objects.filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_de.objects.filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_de.objects.filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_de.objects.filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_de.objects.filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_de.objects.filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_de.objects.filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_de.objects.filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_de.objects.filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_de.objects.filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_de.objects.filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_de.objects.filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_de.objects.filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_de.objects.filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_de.objects.filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_de.objects.filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_de.objects.filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_de.objects.filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_de.objects.filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_de.objects.filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_de.objects.filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_de.objects.filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_de.objects.filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_de.objects.filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_de.objects.filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_de.objects.filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_de.objects.filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_de.objects.filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_de.objects.filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_de.objects.filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_de.objects.filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_de.objects.filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_de.objects.filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_de.objects.filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_de.objects.filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_de.objects.filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_de.objects.filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_de.objects.filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_de.objects.filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_de.objects.filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_de.objects.filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_de.objects.filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_de.objects.filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_de.objects.filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_de.objects.filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_de.objects.filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_de.objects.filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_de.objects.filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_de.objects.filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_de.objects.filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_de.objects.filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_de.objects.filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_de.objects.filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_de.objects.filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_de.objects.filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_de.objects.filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_de.objects.filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_de.objects.filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_de.objects.filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_de.objects.filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_de.objects.filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_de.objects.filter(category='visual').filter(city='').order_by('business_name')
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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_dc.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_dc.objects.filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_dc.objects.filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_dc.objects.filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_dc.objects.filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_dc.objects.filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_dc.objects.filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_dc.objects.filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_dc.objects.filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_dc.objects.filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_dc.objects.filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_dc.objects.filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_dc.objects.filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_dc.objects.filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_dc.objects.filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_dc.objects.filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_dc.objects.filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_dc.objects.filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_dc.objects.filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_dc.objects.filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_dc.objects.filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_dc.objects.filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_dc.objects.filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_dc.objects.filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_dc.objects.filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_dc.objects.filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_dc.objects.filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_dc.objects.filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_dc.objects.filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_dc.objects.filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_dc.objects.filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_dc.objects.filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_dc.objects.filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_dc.objects.filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_dc.objects.filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_dc.objects.filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_dc.objects.filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_dc.objects.filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_dc.objects.filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_dc.objects.filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_dc.objects.filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_dc.objects.filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_dc.objects.filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_dc.objects.filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_dc.objects.filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_dc.objects.filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_dc.objects.filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_dc.objects.filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_dc.objects.filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_dc.objects.filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_dc.objects.filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_dc.objects.filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_dc.objects.filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_dc.objects.filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_dc.objects.filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_dc.objects.filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_dc.objects.filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_dc.objects.filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_dc.objects.filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_dc.objects.filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_dc.objects.filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_dc.objects.filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_dc.objects.filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_dc.objects.filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_dc.objects.filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_dc.objects.filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_dc.objects.filter(category='visual').filter(city='').order_by('business_name')
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
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_fl.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-GA':
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_ga.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-HI':
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_hi.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-ID':
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_id.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-IL':
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_il.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-IN':
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_in.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-IA':
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_ia.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-KS':
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_ks.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-KY':
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_la.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-ME':
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_md.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_md.objects.filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_md.objects.filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_md.objects.filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_md.objects.filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_md.objects.filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_md.objects.filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_md.objects.filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_md.objects.filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_md.objects.filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_md.objects.filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_md.objects.filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_md.objects.filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_md.objects.filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_md.objects.filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_md.objects.filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_md.objects.filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_md.objects.filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_md.objects.filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_md.objects.filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_md.objects.filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_md.objects.filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_md.objects.filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_md.objects.filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_md.objects.filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_md.objects.filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_md.objects.filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_md.objects.filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_md.objects.filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_md.objects.filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_md.objects.filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_md.objects.filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_md.objects.filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_md.objects.filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_md.objects.filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_md.objects.filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_md.objects.filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_md.objects.filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_md.objects.filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_md.objects.filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_md.objects.filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_md.objects.filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_md.objects.filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_md.objects.filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_md.objects.filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_md.objects.filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_md.objects.filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_md.objects.filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_md.objects.filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_md.objects.filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_md.objects.filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_md.objects.filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_md.objects.filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_md.objects.filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_md.objects.filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_md.objects.filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_md.objects.filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_md.objects.filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_md.objects.filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_md.objects.filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_md.objects.filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_md.objects.filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_md.objects.filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_md.objects.filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_md.objects.filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_md.objects.filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_md.objects.filter(category='visual').filter(city='').order_by('business_name')
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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_ma.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ma.objects.filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ma.objects.filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ma.objects.filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ma.objects.filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ma.objects.filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ma.objects.filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ma.objects.filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ma.objects.filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ma.objects.filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ma.objects.filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ma.objects.filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ma.objects.filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ma.objects.filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ma.objects.filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ma.objects.filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ma.objects.filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ma.objects.filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ma.objects.filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ma.objects.filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ma.objects.filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ma.objects.filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ma.objects.filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ma.objects.filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ma.objects.filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ma.objects.filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ma.objects.filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ma.objects.filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ma.objects.filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ma.objects.filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ma.objects.filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ma.objects.filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ma.objects.filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ma.objects.filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ma.objects.filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ma.objects.filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ma.objects.filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ma.objects.filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ma.objects.filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ma.objects.filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ma.objects.filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ma.objects.filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ma.objects.filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ma.objects.filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ma.objects.filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ma.objects.filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ma.objects.filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ma.objects.filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ma.objects.filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ma.objects.filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ma.objects.filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ma.objects.filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ma.objects.filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ma.objects.filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ma.objects.filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ma.objects.filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ma.objects.filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ma.objects.filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ma.objects.filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ma.objects.filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ma.objects.filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ma.objects.filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ma.objects.filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ma.objects.filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ma.objects.filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ma.objects.filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ma.objects.filter(category='visual').filter(city='').order_by('business_name')
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
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_mi.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-MS':
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_ms.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-MN':
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_mo.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-MT':
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_nj.objects.all(),
        beauty_full = vbp_nj.objects.filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_nj.objects.filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_nj.objects.filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_nj.objects.filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_nj.objects.filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_nj.objects.filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_nj.objects.filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_nj.objects.filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_nj.objects.filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_nj.objects.filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_nj.objects.filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_nj.objects.filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_nj.objects.filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_nj.objects.filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_nj.objects.filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_nj.objects.filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_nj.objects.filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_nj.objects.filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_nj.objects.filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_nj.objects.filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_nj.objects.filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_nj.objects.filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_nj.objects.filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_nj.objects.filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_nj.objects.filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_nj.objects.filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_nj.objects.filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_nj.objects.filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_nj.objects.filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_nj.objects.filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_nj.objects.filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_nj.objects.filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_nj.objects.filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_nj.objects.filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_nj.objects.filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_nj.objects.filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_nj.objects.filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_nj.objects.filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_nj.objects.filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_nj.objects.filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_nj.objects.filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_nj.objects.filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_nj.objects.filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_nj.objects.filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_nj.objects.filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_nj.objects.filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_nj.objects.filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_nj.objects.filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_nj.objects.filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_nj.objects.filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_nj.objects.filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_nj.objects.filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_nj.objects.filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_nj.objects.filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_nj.objects.filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_nj.objects.filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_nj.objects.filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_nj.objects.filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_nj.objects.filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_nj.objects.filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_nj.objects.filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_nj.objects.filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_nj.objects.filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_nj.objects.filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_nj.objects.filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_nj.objects.filter(category='visual').filter(city='').order_by('business_name')
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_ny.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_ny.objects.filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_ny.objects.filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_ny.objects.filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_ny.objects.filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_ny.objects.filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_ny.objects.filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_ny.objects.filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_ny.objects.filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_ny.objects.filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_ny.objects.filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_ny.objects.filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_ny.objects.filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_ny.objects.filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_ny.objects.filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_ny.objects.filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_ny.objects.filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_ny.objects.filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_ny.objects.filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_ny.objects.filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_ny.objects.filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_ny.objects.filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_ny.objects.filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_ny.objects.filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_ny.objects.filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_ny.objects.filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_ny.objects.filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_ny.objects.filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_ny.objects.filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_ny.objects.filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_ny.objects.filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_ny.objects.filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_ny.objects.filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_ny.objects.filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_ny.objects.filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_ny.objects.filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_ny.objects.filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_ny.objects.filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_ny.objects.filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_ny.objects.filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_ny.objects.filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_ny.objects.filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_ny.objects.filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_ny.objects.filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_ny.objects.filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_ny.objects.filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_ny.objects.filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_ny.objects.filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_ny.objects.filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_ny.objects.filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_ny.objects.filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_ny.objects.filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_ny.objects.filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_ny.objects.filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_ny.objects.filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_ny.objects.filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_ny.objects.filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_ny.objects.filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_ny.objects.filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_ny.objects.filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_ny.objects.filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_ny.objects.filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_ny.objects.filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_ny.objects.filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_ny.objects.filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_ny.objects.filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_ny.objects.filter(category='visual').filter(city='').order_by('business_name')
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_oh.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_oh.objects.filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_oh.objects.filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_oh.objects.filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_oh.objects.filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_oh.objects.filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_oh.objects.filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_oh.objects.filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_oh.objects.filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_oh.objects.filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_oh.objects.filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_oh.objects.filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_oh.objects.filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_oh.objects.filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_oh.objects.filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_oh.objects.filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_oh.objects.filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_oh.objects.filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_oh.objects.filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_oh.objects.filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_oh.objects.filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_oh.objects.filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_oh.objects.filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_oh.objects.filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_oh.objects.filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_oh.objects.filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_oh.objects.filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_oh.objects.filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_oh.objects.filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_oh.objects.filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_oh.objects.filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_oh.objects.filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_oh.objects.filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_oh.objects.filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_oh.objects.filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_oh.objects.filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_oh.objects.filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_oh.objects.filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_oh.objects.filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_oh.objects.filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_oh.objects.filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_oh.objects.filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_oh.objects.filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_oh.objects.filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_oh.objects.filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_oh.objects.filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_oh.objects.filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_oh.objects.filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_oh.objects.filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_oh.objects.filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_oh.objects.filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_oh.objects.filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_oh.objects.filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_oh.objects.filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_oh.objects.filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_oh.objects.filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_oh.objects.filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_oh.objects.filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_oh.objects.filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_oh.objects.filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_oh.objects.filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_oh.objects.filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_oh.objects.filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_oh.objects.filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_oh.objects.filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_oh.objects.filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_oh.objects.filter(category='visual').filter(city='').order_by('business_name')
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_pa.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_pa.objects.filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_pa.objects.filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_pa.objects.filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_pa.objects.filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_pa.objects.filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_pa.objects.filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_pa.objects.filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_pa.objects.filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_pa.objects.filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_pa.objects.filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_pa.objects.filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_pa.objects.filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_pa.objects.filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_pa.objects.filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_pa.objects.filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_pa.objects.filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_pa.objects.filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_pa.objects.filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_pa.objects.filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_pa.objects.filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_pa.objects.filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_pa.objects.filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_pa.objects.filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_pa.objects.filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_pa.objects.filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_pa.objects.filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_pa.objects.filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_pa.objects.filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_pa.objects.filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_pa.objects.filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_pa.objects.filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_pa.objects.filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_pa.objects.filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_pa.objects.filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_pa.objects.filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_pa.objects.filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_pa.objects.filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_pa.objects.filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_pa.objects.filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_pa.objects.filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_pa.objects.filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_pa.objects.filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_pa.objects.filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_pa.objects.filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_pa.objects.filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_pa.objects.filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_pa.objects.filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_pa.objects.filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_pa.objects.filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_pa.objects.filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_pa.objects.filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_pa.objects.filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_pa.objects.filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_pa.objects.filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_pa.objects.filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_pa.objects.filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_pa.objects.filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_pa.objects.filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_pa.objects.filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_pa.objects.filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_pa.objects.filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_pa.objects.filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_pa.objects.filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_pa.objects.filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_pa.objects.filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_pa.objects.filter(category='visual').filter(city='').order_by('business_name')
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_sc.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-SD':
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
        state_qs = vbp_tn.objects.all().order_by('category', 'city', 'business_name'),
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
    if state == 'US-TX':
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
        state_qs = list(vbp_va.objects.all().order_by('category', 'city', 'business_name')),
        beauty_full = vbp_va.objects.filter(category='beauty').exclude(city='').order_by('city', 'business_name')
        beauty_blank = vbp_va.objects.filter(category='beauty').filter(city='').order_by('business_name')
        beauty = list(beauty_full) + list(beauty_blank)
        books_full = vbp_va.objects.filter(category='books').exclude(city='').order_by('city', 'business_name')
        books_blank = vbp_va.objects.filter(category='books').filter(city='').order_by('business_name')
        books = list(books_full) + list(books_blank)
        cars_full = vbp_va.objects.filter(category='cars').exclude(city='').order_by('city', 'business_name')
        cars_blank = vbp_va.objects.filter(category='cars').filter(city='').order_by('business_name')
        cars = list(cars_full) + list(cars_blank)
        child_full = vbp_va.objects.filter(category='child').exclude(city='').order_by('city', 'business_name')
        child_blank = vbp_va.objects.filter(category='child').filter(city='').order_by('business_name')
        child = list(child_full) + list(child_blank)
        cleaning_full = vbp_va.objects.filter(category='cleaning').exclude(city='').order_by('city', 'business_name')
        cleaning_blank = vbp_va.objects.filter(category='cleaning').filter(city='').order_by('business_name')
        cleaning = list(cleaning_full) + list(cleaning_blank)
        clothing_full = vbp_va.objects.filter(category='clothing').exclude(city='').order_by('city', 'business_name')
        clothing_blank = vbp_va.objects.filter(category='clothing').filter(city='').order_by('business_name')
        clothing = list(clothing_full) + list(clothing_blank)
        construction_full = vbp_va.objects.filter(category='construction').exclude(city='').order_by('city', 'business_name')
        construction_blank = vbp_va.objects.filter(category='construction').filter(city='').order_by('business_name')
        construction = list(construction_full) + list(construction_blank)
        education_full = vbp_va.objects.filter(category='education').exclude(city='').order_by('city', 'business_name')
        education_blank = vbp_va.objects.filter(category='education').filter(city='').order_by('business_name')
        education = list(education_full) + list(education_blank)
        eldercare_full = vbp_va.objects.filter(category='eldercare').exclude(city='').order_by('city', 'business_name')
        eldercare_blank = vbp_va.objects.filter(category='eldercare').filter(city='').order_by('business_name')
        eldercare = list(eldercare_full) + list(eldercare_blank)
        electronics_full = vbp_va.objects.filter(category='electronics').exclude(city='').order_by('city', 'business_name')
        electronics_blank = vbp_va.objects.filter(category='electronics').filter(city='').order_by('business_name')
        electronics = list(electronics_full) + list(electronics_blank)
        entertainment_full = vbp_va.objects.filter(category='entertainment').exclude(city='').order_by('city', 'business_name')
        entertainment_blank = vbp_va.objects.filter(category='entertainment').filter(city='').order_by('business_name')
        entertainment = list(entertainment_full) + list(entertainment_blank)
        farming_full = vbp_va.objects.filter(category='farming').exclude(city='').order_by('city', 'business_name')
        farming_blank = vbp_va.objects.filter(category='farming').filter(city='').order_by('business_name')
        farming = list(farming_full) + list(farming_blank)
        florists_full = vbp_va.objects.filter(category='florists').exclude(city='').order_by('city', 'business_name')
        florists_blank = vbp_va.objects.filter(category='florists').filter(city='').order_by('business_name')
        florists = list(florists_full) + list(florists_blank)
        grocery_full = vbp_va.objects.filter(category='grocery').exclude(city='').order_by('city', 'business_name')
        grocery_blank = vbp_va.objects.filter(category='grocery').filter(city='').order_by('business_name')
        grocery = list(grocery_full) + list(grocery_blank)
        health_full = vbp_va.objects.filter(category='health').exclude(city='').order_by('city', 'business_name')
        health_blank = vbp_va.objects.filter(category='health').filter(city='').order_by('business_name')
        health = list(health_full) + list(health_blank)
        home_full = vbp_va.objects.filter(category='home').exclude(city='').order_by('city', 'business_name')
        home_blank = vbp_va.objects.filter(category='home').filter(city='').order_by('business_name')
        home = list(home_full) + list(home_blank)
        hotels_full = vbp_va.objects.filter(category='hotels').exclude(city='').order_by('city', 'business_name')
        hotels_blank = vbp_va.objects.filter(category='hotels').filter(city='').order_by('business_name')
        hotels = list(hotels_full) + list(hotels_blank)
        jewelry_full = vbp_va.objects.filter(category='jewelry').exclude(city='').order_by('city', 'business_name')
        jewelry_blank = vbp_va.objects.filter(category='jewelry').filter(city='').order_by('business_name')
        jewelry = list(jewelry_full) + list(jewelry_blank)
        legal_full = vbp_va.objects.filter(category='legal').exclude(city='').order_by('city', 'business_name')
        legal_blank = vbp_va.objects.filter(category='legal').filter(city='').order_by('business_name')
        legal = list(legal_full) + list(legal_blank)
        lifestyle_full = vbp_va.objects.filter(category='lifestyle').exclude(city='').order_by('city', 'business_name')
        lifestyle_blank = vbp_va.objects.filter(category='lifestyle').filter(city='').order_by('business_name')
        lifestyle = list(lifestyle_full) + list(lifestyle_blank)
        marketing_full = vbp_va.objects.filter(category='marketing').exclude(city='').order_by('city', 'business_name')
        marketing_blank = vbp_va.objects.filter(category='marketing').filter(city='').order_by('business_name')
        marketing = list(marketing_full) + list(marketing_blank)
        medical_full = vbp_va.objects.filter(category='medical').exclude(city='').order_by('city', 'business_name')
        medical_blank = vbp_va.objects.filter(category='medical').filter(city='').order_by('business_name')
        medical = list(medical_full) + list(medical_blank)
        other_full = vbp_va.objects.filter(category='other').exclude(city='').order_by('city', 'business_name')
        other_blank = vbp_va.objects.filter(category='other').filter(city='').order_by('business_name')
        other = list(other_full) + list(other_blank)
        packaging_full = vbp_va.objects.filter(category='packaging').exclude(city='').order_by('city', 'business_name')
        packaging_blank = vbp_va.objects.filter(category='packaging').filter(city='').order_by('business_name')
        packaging = list(packaging_full) + list(packaging_blank)
        pets_full = vbp_va.objects.filter(category='pets').exclude(city='').order_by('city', 'business_name')
        pets_blank = vbp_va.objects.filter(category='pets').filter(city='').order_by('business_name')
        pets = list(pets_full) + list(pets_blank)
        photography_full = vbp_va.objects.filter(category='photography').exclude(city='').order_by('city', 'business_name')
        photography_blank = vbp_va.objects.filter(category='photography').filter(city='').order_by('business_name')
        photography = list(photography_full) + list(photography_blank)
        professional_full = vbp_va.objects.filter(category='professional').exclude(city='').order_by('city', 'business_name')
        professional_blank = vbp_va.objects.filter(category='professional').filter(city='').order_by('business_name')
        professional = list(professional_full) + list(professional_blank)
        realestate_full = vbp_va.objects.filter(category='realestate').exclude(city='').order_by('city', 'business_name')
        realestate_blank = vbp_va.objects.filter(category='realestate').filter(city='').order_by('business_name')
        realestate = list(realestate_full) + list(realestate_blank)
        recreation_full = vbp_va.objects.filter(category='recreation').exclude(city='').order_by('city', 'business_name')
        recreation_blank = vbp_va.objects.filter(category='recreation').filter(city='').order_by('business_name')
        recreation = list(recreation_full) + list(recreation_blank)
        restaurants_full = vbp_va.objects.filter(category='restaurants').exclude(city='').order_by('city', 'business_name')
        restaurants_blank = vbp_va.objects.filter(category='restaurants').filter(city='').order_by('business_name')
        restaurants = list(restaurants_full) + list(restaurants_blank)
        security_full = vbp_va.objects.filter(category='security').exclude(city='').order_by('city', 'business_name')
        security_blank = vbp_va.objects.filter(category='security').filter(city='').order_by('business_name')
        security = list(security_full) + list(security_blank)
        transportation_full = vbp_va.objects.filter(category='transportation').exclude(city='').order_by('city', 'business_name')
        transportation_blank = vbp_va.objects.filter(category='transportation').filter(city='').order_by('business_name')
        transportation = list(transportation_full) + list(transportation_blank)
        visual_full = vbp_va.objects.filter(category='visual').exclude(city='').order_by('city', 'business_name')
        visual_blank = vbp_va.objects.filter(category='visual').filter(city='').order_by('business_name')
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
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
        covers_qs = vbp_book.objects.all()
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