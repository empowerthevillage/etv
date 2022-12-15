import django
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Q

from .models import mv_private, vbp_book, vbp_nj, vbp_ct, gift_guide, StateFilter  
from django.core.paginator import Paginator
from django.conf import settings

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
BOOK_CHOICES = [
    ("bookstore", "Book Store"),
    ("onlinepub", "Online Publication"),
    ("publishing", "Publishing"),
    ("authors", "Authors"),
    ("other", "Other"),
]
CARS_CHOICES = [
    ("autodealership", "Auto Dealership"),
    ("autorepair", "Auto Repair/ Services"),
    ("carwash", "Car Wash"),
    ("gasstation", "Gas Station"),
    ("other", "Other"),
]
CHILD_CHOICES = [
    ("babyproducts", "Baby Products"),
    ("childcare", "Childcare/Daycare/ Preschool"),
    ("childbooks", "Children’s Books"),
    ("childactivities", "Children’s Activities"),
    ("other", "Other"),
]
CLEANING_CHOICES = [
    ("cleaningproducts", "Cleaning Products"),
    ("drycleaning", "Dry Cleaning"),
    ("laundry", "Laundry"),
    ("other", "Other"),
]
CLOTHING_CHOICES = [
    ("apparel", "Apparel"),
    ("stylist", "Stylist"),
    ("footwear", "Footwear"),
    ("fabric", "Fabric/Yarn"),
    ("other", "Other"),
]
CONSTRUCTION_CHOICES = [
    ("appliancerepair", "Appliance Repair"),
    ("construction", "Construction/ Engineering"),
    ("electrical", "Electrical"),
    ("hvac", "HVAC"),
    ("plumbing", "Plumbing"),
    ("powerwashing", "Power Washing"),
    ("roofing", "Roofing & Siding"),
    ("paintingservices", "Painting Services"),
    ("other", "Other"),
]
EDUCATION_CHOICES = [
    ("tutor", "Tutoring/ Academic Planning"),
    ("driving", "Driving/ Aviation"),
    ("enrichment", "Enrichment"),
    ("other", "Other"),
]
ELDERCARE_CHOICES = [
    ("assistedliving", "Assisted Living/Nursing Home"),
    ("homehealth", "Home Health Care/ Nursing Services"),
    ("adultdaycare", "Adult Day Care Center"),
    ("other", "Other"),
]
ELECTRONICS_CHOICES = [
    ("cybersecurity", "Cybersecurity"),
    ("software", "Software Development"),
    ("techsupport", "Tech Support/ Repair"),
    ("techproducts", "Tech Products"),
    ("webservices", "Web Services"),
    ("other", "Other"),
]
ENTERTAINMENT_CHOICES = [
    ("bands", "Bands/DJs/Performers"),
    ("comedian", "Comedian"),
    ("eventplanning", "Event Planning/Services"),
    ("media", "Media"),
    ("paintnsip", "Paint & Sip"),
    ("other", "Other"),
]
FARMING_CHOICES = [
    ("farmersmarket", "Farmer’s Market"),
    ("vineyard", "Vineyard"),
    ("other", "Other"),
]
GROCERY_CHOICES = [
    ("bakery", "Bakery"),
    ("catering", "Catering/ Chef"),
    ("coffee", "Coffee/Tea/Beverages"),
    ("fooddelivery", "Food Delivery Service"),
    ("icecream", "Ice Cream Parlor"),
    ("alcohol", "Alcohol"),
    ("specialty", "Specialty"),
    ("other", "Other"),
]
HEALTH_CHOICES = [
    ("addiction", "Addiction Treatment"),
    ("chiropractor", "Chiropractor"),
    ("fitness", "Fitness/ Yoga"),
    ("spa", "Spa/ Massage Therapy"),
    ("mentalhealth", "Mental Health Support"),
    ("nutrition", "Nutrition"),
    ("other", "Other"),
]
HOME_CHOICES = [
    ("furniture", "Furniture"),
    ("landscaping", "Landscaping/Gardening"),
    ("interiordesign", "Interior Design/ Home Staging"),
    ("pestcontrol", "Pest Control"),
    ("homegoods", "Home Goods/Décor"),
    ("other", "Other"),
]
HOTEL_CHOICES = [
    ("travelagent", "Travel Agent"),
    ("hospitality", "Hospitality/Hotels/Inns"),
    ("tours", "Tours"),
    ("other", "Other"),
]
JEWELRY_CHOICES = [
    ("accessories", "Accessories/ Handbags"),
    ("finejewelry", "Fine Jewelry"),
    ("other", "Other"),
]
LEGAL_CHOICES = [
    ("financialservices", "Financial Services"),
    ("notary", "Notary"),
    ("bail", "Bail Bonds Service"),
    ("legal", "Legal Services (General)"),
    ("realestatelaw", "Real Estate Law"),
    ("estateplanning", "Estate Planning/Wills"),
    ("corporatelaw", "Corporate Law"),
    ("insurance", "Insurance"),
    ("other", "Other"),
]
LIFESTYLE_CHOICES = [
    ("adultnovelties", "Adult Novelties"),
    ("cbd", "CBD Products"),
    ("smoking", "Smoking & Paraphernalia"),
    ("tarot", "Tarot"),
    ("piercing", "Piercing/ Tattoos"),
    ("other", "Other"),
]
MARKETING_CHOICES = [
    ("advertising", "Advertising"),
    ("branding", "Branding/ Graphic Design"),
    ("marketing", "Marketing/ Digital Marketing"),
    ("webservices", "Web Services/ Social Media"),
    ("other", "Other"),
]
MEDICAL_CHOICES = [
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
]
OTHER_CHOICES = [
    ("antiques", "Antiques & Collectibles"),
    ("guns", "Guns & Shooting Ranges"),
    ("gifts", "Gifts & Stationery"),
    ("mortuary", "Mortuary/ Funeral Services"),
    ("marketplace", "Marketplace"),
    ("translation", "Translation Services"),
    ("officesupplies", "Office Supplies"),
    ("other", "Other"),
]
PACKAGING_CHOICES = [
    ("courier", "Courier"),
    ("printing", "Printing"),
    ("shipping", "Shipping"),
    ("other", "Other"),
]
PETS_CHOICES = [
    ("dogtraining", "Dog Training"),
    ("petsitting", "Pet Sitting/ Walking"),
    ("vet", "Veterinarian"),
    ("petgrooming", "Pet Grooming"),
    ("other", "Other"),
]
PHOTOGRAPHY_CHOICES = [
    ("videography", "Videography"),
    ("photography", "Photography"),
    ("other", "Other"),
]
PROFESSIONAL_CHOICES = [
    ("consulting", "Consulting"),
    ("humanresources", "Human Resources"),
    ("it", "IT"),
    ("recruiting", "Recruiting/ Staffing"),
    ("privateinvestigator", "Private Investigator"),
    ("writingservices", "Writing Services"),
    ("speakers", "Speakers"),
    ("adminsupport", "Administrative Support"),
    ("other", "Other"),
]
REALESTATE_CHOICES = [
    ("developers", "Developers"),
    ("homeinspection", "Home Inspection"),
    ("mortgageconsulting", "Mortgage Consulting"),
    ("propertymanagement", "Property Management"),
    ("realestateagents", "Real Estate Agents/ Brokers"),
    ("titleservices", "Title Services"),
    ("other", "Other"),
]
RECREATION_CHOICES = [
    ("arcade", "Arcade/Laser Tag"),
    ("sports", "Sports"),
    ("martialarts", "Martial Arts"),
    ("sportsequipment", "Sports Equipment"),
    ("pooltables", "Pool Tables"),
    ("gaming", "Gaming"),
    ("other", "Other"),
]
RESTAURANT_CHOICES = [
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
]
TRANSPORTATION_CHOICES = [
    ("commuter", "Commuter/Shuttle Services"),
    ("mortuarytransport", "Mortuary Transport"),
    ("moving", "Moving Services"),
    ("parking", "Parking"),
    ("taxi", "Taxi"),
    ("limo", "Limo/ Party Bus"),
    ("trucking", "Trucking"),
    ("valet", "Valet"),
    ("other", "Other"),
]
VISUAL_CHOICES = [
    ("artgallery", "Art Gallery/ Museum"),
    ("dance", "Dance Studios/Lessons"),
    ("artists", "Artists"),
    ("theater", "Theater/Acting Lessons"),
    ("music", "Music Lessons/Instruments"),
    ("other", "Other"),
]
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
CATEGORY_JSON = [
  {'beauty':'Beauty & Personal Grooming'},
  {'books':'Books & Publishing'},
  {'cars':'Cars & Automotive'},
  {'child':"Childcare | Children's Services & Products"},
  {'cleaning':"Cleaning"},
  {'clothing':"Clothing & Fashion"},
  {'construction':"Construction & Trades"},
  {'education':"Education"},
  {'eldercare':"Eldercare"},
  {'electronics':"Electronics & Technology"},
  {'entertainment':"Entertainment"},
  {'farming':"Farming & Agriculture"},
  {'florists':"Florists"},
  {'grocery':"Grocery & Food Services"},
  {'health':"Health & Wellness"},
  {'home':"Home & Garden"},
  {'hotels':"Hotels & Hospitality | Travel"},
  {'jewelry':"Jewelry & Accessories"},
  {'legal':"Legal & Financial Services"},
  {'lifestyle':"Lifestyle"},
  {'marketing':"Marketing & Advertising"},
  {'medical':"Medical Services"},
  {'packaging':"Packaging | Delivery | Shipping"},
  {'pets':"Pets & Animal Care"},
  {'photography':"Photography & Video"},
  {'professional':"Professional Services"},
  {'real estate':"Real Estate"},
  {'recreation':"Recreation & Sports"},
  {'restaurants':"Restaurants & Bars | Event Spaces"},
  {'security':"Security Services"},
  {'transportation':"Transportation & Trucking"},
  {'visual':"Visual & Performing Arts | Culture"},
  {'other':"Other"},
]

def mv_view(request):
    f = mv_private.objects.all()
    listings_full = f.exclude(city='').order_by('category', 'cat_ordering', 'city', 'business_name')
    listings_empty = f.filter(city='').order_by('category', 'cat_ordering', 'business_name')
    all_listings = list(listings_full) + list(listings_empty)
    sections = []
    page_count = 5
    for category, verbose in CATEGORY_CHOICES:
        dict = []
        for x in all_listings:
            if x.category == category:
                dict.append(x)
        if len(dict)>0:
            pagination_obj = Paginator(dict, 16)
            start_page = page_count + 1
            page_count += pagination_obj.num_pages
            line = {"category": category, "verbose": str(verbose), "pagination": pagination_obj, "start_page": start_page, "last_page": page_count, "cover": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s.svg" %(str(verbose)), "right": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_right.svg" %(str(verbose)),"left": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_left.svg" %(str(verbose))}
            sections.append(line)
        else:
            pass
    
    col_1_end = round(len(sections)/2)
    col_2_start = col_1_end + 1
    col_2_end = len(sections)
    col1 = sections[0:col_1_end]
    col2 = sections[col_2_start:col_2_end]
    context = {
        "sections": sections,
        "col1": col1,
        "col2":  col2,
        "filter": f,
    }
    return render(request, 'vbp/mv.html', context)

def get_subcats(request):
  if request.method == 'POST':
    categories = request.POST['categories']
    c_split = categories.split(',')
    verboses = request.POST['verboseList']
    v_split = verboses.split(',')
    merged = zip(c_split, v_split)
    formatted = list(merged)
    sections = []
    for cat in formatted:
        category = cat[0]
        verbose = cat[1]
        subcategories = list(vbp_nj.objects.filter(category=str(category)).order_by('subcategory').distinct('subcategory'))
        
        sections.append({'category': category, 'verbose': verbose, 'subcategories': subcategories})
    context = {
      'sections': sections
    }
    html = render_to_string('vbp/subcategory-filter.html', context)
    return JsonResponse({'status':'success', 'html':html})
  else:
    return JsonResponse({'status':'error'})

def nj_filter_new(request):
    if request.method == 'POST':
        categories = request.POST['catList'].split(',')
        subcategories = request.POST['subcatList'].split(',')
        cities = request.POST['cityList'].split(',')
        counties = request.POST['countyList'].split(',')
        if counties != [''] or cities !=[''] and subcategories != [''] and categories !=['']:
          result = vbp_nj.objects.filter(Q(county__in=counties)|Q(city__in=cities),Q(subcategory__in=subcategories)|Q(category__in=categories))
        elif counties != [''] or cities !=[''] and subcategories == [''] and categories == ['']:
          result = vbp_nj.objects.filter(Q(county__in=counties)|Q(city__in=cities))
        elif counties == [''] and cities !=[''] and subcategories == [''] and categories ==['']:
          result = vbp_nj.objects.filter(Q(city__in=cities))
        elif counties !=[''] and cities == [''] and subcategories == [''] and categories == ['']:
          result = vbp_nj.objects.filter(Q(county__in=counties))
        elif counties == [''] and cities == [''] and subcategories == [''] and categories != ['']:
          result = vbp_nj.objects.filter(Q(category__in=categories))
        elif counties == [''] and cities == [''] and subcategories != [''] and categories == ['']:
          result = vbp_nj.objects.filter(Q(subcategory__in=subcategories))
        elif counties == [''] and cities == [''] and subcategories !=[''] and categories !=['']:
          result = vbp_nj.objects.filter(Q(subcategory__in=subcategories),Q(category__in=categories))
          
        f = vbp_nj.objects.filter(approved=True)
        listings_beauty = result.filter(category='beauty').order_by('group', 'subcategory', '-city', 'business_name')
   
        listings_full = result.exclude(city='').exclude(category='beauty').order_by('category', 'city', 'business_name')
        listings_empty = result.filter(city='').exclude(category='beauty').order_by('category', 'business_name')

      
        all_listings = list(listings_beauty) + list(listings_full) + list(listings_empty)
        sections = []
        page_count = 5
        cities = []
        counties = []
        cats = []
        for x in f:
          if x.city not in cities:
            cities.append(x.city)
          if x.county not in counties:
            counties.append(x.county)
          
        city_dict = sorted(cities)
        county_dict = sorted(counties)
        for category, verbose in CATEGORY_CHOICES:
            if x.category not in cats:
              line = {"category": category, "verbose":verbose}
              cats.append(line)
            dict = []
            subcats = []
            for x in all_listings:
                if x.category == category:
                    dict.append(x)
                    if x.subcategory not in subcats:
                      if x.subcategory is not None:
                        subcats.append(x.subcategory)
            if len(dict)>0:
                if category == 'beauty':
                    pagination_obj = Paginator(dict, 11)
                else:
                    pagination_obj = Paginator(dict, 16)
                start_page = page_count + 1
                page_count += pagination_obj.num_pages
                line = {"category": category, "subcats": sorted(subcats), "verbose": str(verbose), "pagination": pagination_obj, "start_page": start_page, "last_page": page_count, "cover": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s.svg" %(str(verbose)), "right": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_right.svg" %(str(verbose)),"left": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_left.svg" %(str(verbose))}
                sections.append(line)
            else:
                pass
          
        col_1_end = round(len(sections)/2)
        col_2_start = col_1_end + 1
        col_2_end = len(sections)
        col1 = sections[0:col_1_end]
        col2 = sections[col_2_start:col_2_end]
        context = {
            "cities": city_dict,
            "counties": county_dict,
            "sections": sections,
            "col1": col1,
            "col2":  col2,
            "filter": f,
            "cats": cats,
        }
    html = render_to_string('vbp/nj_filtered.html',context)
    return JsonResponse({'status':'success',"html":html})
      
def nj_view(request):
    f = vbp_nj.objects.filter(approved=True)
    
    listings_beauty = f.filter(category='beauty').order_by('group', 'subcategory', '-city', 'business_name')
   
    listings_full = f.exclude(city='').exclude(category='beauty').order_by('category', 'city', 'business_name')
    listings_empty = f.filter(city='').exclude(category='beauty').order_by('category', 'business_name')

    
    all_listings = list(listings_beauty) + list(listings_full) + list(listings_empty)
    sections = []
    page_count = 5
    cities = []
    counties = []
    for x in all_listings:
      if x.city not in cities:
        cities.append(x.city)
      if x.county not in counties:
        counties.append(x.county)
    city_dict = sorted(cities)
    county_dict = sorted(counties)
    for category, verbose in CATEGORY_CHOICES:
        dict = []
        subcats = []
        for x in all_listings:
            if x.category == category:
                dict.append(x)
                if x.subcategory not in subcats:
                  if x.subcategory is not None:
                    subcats.append(x.subcategory)
        if len(dict)>0:
            if category == 'beauty':
                pagination_obj = Paginator(dict, 11)
            else:
                pagination_obj = Paginator(dict, 16)
            start_page = page_count + 1
            page_count += pagination_obj.num_pages
            line = {"category": category, "subcats": sorted(subcats), "verbose": str(verbose), "pagination": pagination_obj, "start_page": start_page, "last_page": page_count, "cover": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s.svg" %(str(verbose)), "right": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_right.svg" %(str(verbose)),"left": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_left.svg" %(str(verbose))}
            sections.append(line)
        else:
            pass
    
    col_1_end = round(len(sections)/2)
    col_2_start = col_1_end + 1
    col_2_end = len(sections)
    col1 = sections[0:col_1_end]
    col2 = sections[col_2_start:col_2_end]
    context = {
        "cities": city_dict,
        "counties": county_dict,
        "sections": sections,
        "col1": col1,
        "col2":  col2,
        "filter": f,
    }
    return render(request, 'vbp/nj_only.html', context)

def nj_new(request):
  f = vbp_nj.objects.filter()
  cats = []
  for (category,verbose) in CATEGORY_CHOICES:
    listings = vbp_nj.objects.filter(Q(category__exact=category))
    cats.append({'category':category,'listings':listings})
  print(cats)
  return render(request, 'vbp/nj_only.html')
  
def gift_guide_view(request):
    listings = gift_guide.objects.filter(approved=True)
    page1 = {
        'object_list': listings[0:7],
        'has_ad': False,
        'ad': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gift-guide-1.webp',
    }
    page2 = {
        'object_list': listings[7:19],
        'has_ad': False,
        'ad': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gift-guide-2.webp'
    }
    page3 = {
        'object_list': listings[19:29],
        'has_ad': False,
    }
    page4 = {
        'object_list': listings[29:38],
        'has_ad': False,
        'ad': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gift-guide-3.webp'
    }
    pages = [page1, page2, page3, page4]
    
    mpage1 = {
        'object_list': listings[0:9],
        'has_ad': False,
        'ad': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gift-guide-1.webp',
    }
    mpage2 = {
        'object_list': listings[9:18],
        'has_ad': False,
        'ad': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gift-guide-2.webp'
    }
    mpage3 = {
        'object_list': listings[18:22],
        'has_ad': False,
    }
    mpage4 = {
        'object_list': listings[22:36],
        'has_ad': False,
        'ad': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gift-guide-3.webp'
    }
    mpages = [mpage1, mpage2, mpage3, mpage4]
    
    
    context = {
        'pages': pages,
        'mpages': mpages,
    }
    return render(request, 'gift-guide.html', context)

def listing_filter(request, state):
    state_formatted = state.split("-")[1].lower()
    model = django.apps.apps.get_model('vbp', 'vbp_%s' %(state_formatted))
    data = request.GET
    f = StateFilter(data, queryset=model.objects.order_by('cat_ordering','city', 'business_name'))
    filtered_qs = f.qs
    beauty = filtered_qs.filter(approved=True).filter(category='beauty').order_by('cat_ordering','city', 'business_name')
    books = filtered_qs.filter(approved=True).filter(category='books').order_by('cat_ordering','city', 'business_name')
    cars = filtered_qs.filter(approved=True).filter(category='cars').order_by('cat_ordering','city', 'business_name')
    child = filtered_qs.filter(approved=True).filter(category='child').order_by('cat_ordering','city', 'business_name')
    cleaning = filtered_qs.filter(approved=True).filter(category='cleaning').order_by('cat_ordering','city', 'business_name')
    clothing = filtered_qs.filter(approved=True).filter(category='clothing').order_by('cat_ordering','city', 'business_name')
    construction = filtered_qs.filter(approved=True).filter(category='construction').order_by('cat_ordering','city', 'business_name')
    education = filtered_qs.filter(approved=True).filter(category='education').order_by('cat_ordering','city', 'business_name')
    eldercare = filtered_qs.filter(approved=True).filter(category='eldercare').order_by('cat_ordering','city', 'business_name')
    electronics = filtered_qs.filter(approved=True).filter(category='electronics').order_by('cat_ordering','city', 'business_name')
    entertainment = filtered_qs.filter(approved=True).filter(category='entertainment').order_by('cat_ordering','city', 'business_name')
    farming = filtered_qs.filter(approved=True).filter(category='farming').order_by('cat_ordering','city', 'business_name')
    florists = filtered_qs.filter(approved=True).filter(category='florists').order_by('cat_ordering','city', 'business_name')
    grocery = filtered_qs.filter(approved=True).filter(category='grocery').order_by('cat_ordering','city', 'business_name')
    health = filtered_qs.filter(approved=True).filter(category='health').order_by('cat_ordering','city', 'business_name')
    home = filtered_qs.filter(approved=True).filter(category='home').order_by('cat_ordering','city', 'business_name')
    hotels = filtered_qs.filter(approved=True).filter(category='hotels').order_by('cat_ordering','city', 'business_name')
    jewelry = filtered_qs.filter(approved=True).filter(category='jewelry').order_by('cat_ordering','city', 'business_name')
    legal = filtered_qs.filter(approved=True).filter(category='legal').order_by('cat_ordering','city', 'business_name')
    lifestyle = filtered_qs.filter(approved=True).filter(category='lifestyle').order_by('cat_ordering','city', 'business_name')
    marketing = filtered_qs.filter(approved=True).filter(category='marketing').order_by('cat_ordering','city', 'business_name')
    medical = filtered_qs.filter(approved=True).filter(category='medical').order_by('cat_ordering','city', 'business_name')
    other = filtered_qs.filter(approved=True).filter(category='other').order_by('cat_ordering','city', 'business_name')
    packaging = filtered_qs.filter(approved=True).filter(category='packaging').order_by('cat_ordering','city', 'business_name')
    pets = filtered_qs.filter(approved=True).filter(category='pets').order_by('cat_ordering','city', 'business_name')
    photography = filtered_qs.filter(approved=True).filter(category='photography').order_by('cat_ordering','city', 'business_name')
    professional = filtered_qs.filter(approved=True).filter(category='professional').order_by('cat_ordering','city', 'business_name')
    realestate = filtered_qs.filter(approved=True).filter(category='real estate').order_by('cat_ordering','city', 'business_name')
    recreation = filtered_qs.filter(approved=True).filter(category='recreation').order_by('cat_ordering','city', 'business_name')
    restaurants = filtered_qs.filter(approved=True).filter(category='restaurants').order_by('cat_ordering','city', 'business_name')
    security = filtered_qs.filter(approved=True).filter(category='security').order_by('cat_ordering','city', 'business_name')
    transportation = filtered_qs.filter(approved=True).filter(category='transportation').order_by('cat_ordering','city', 'business_name')
    visual = filtered_qs.filter(approved=True).filter(category='visual').order_by('cat_ordering','city', 'business_name')

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
    unfiltered_qs = model.objects.all()
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

def get_counties(request, state):
    model = django.apps.apps.get_model('vbp', 'vbp_%s' %(state))
    qs = model.objects.all()
    for i in qs:
        if not i.county:
            try:
                city = i.city
                api_key = str(settings.GEOCODER_KEY)
                geocode_result = geocoder.google(city+", "+state, key=api_key)
                county = geocode_result.current_result.county
                i.county = county
                i.save()
                print(i.county)
            except:
                print('no county')
    return HttpResponse('Counties updated!')

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
    covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
    books = vbp_book.objects.all()
    phase_one_states = [
        "TX",
        "FL",
        "NY",
        "GA",
        "CA",
        "NC",
        "IL",
        "MD",
        "VA",
        "PA",
        "OH",
        "LA",
        "MI",
        "NJ",
        "SC",
        "AL",
        "TN",
        "MS",
        "MO",
        "IN",
        "MA",
        "AR",
        "CT",
        "DC",
        "DE",
        ]
    mapPubValues = {}
    markers = []
    for x in books:
        if str(x) in phase_one_states:
            if x.published == True:
                y = 'published'
            else:
                y = 'soon'
                markers.append(x)
                
            mapPubValues.update({'US-%s' %(x): y})
    return render(
        request, 
        'vbp_list copy.html', 
        {
        'covers_qs': covers_qs,
        'title': 'ETV | Village Black Pages',
        'mapPubValues': mapPubValues,
        'markers': markers
        }
    )

def getStateListings(request):
    state = request.GET['state']
    state_formatted = state.split("-")[1].lower()
    model = django.apps.apps.get_model('vbp', 'vbp_%s' %(state_formatted))
    covers_qs = vbp_book.objects.filter(published=True).order_by('-featured', 'state')
    state_qs = list(model.objects.all().order_by('category', 'city', 'business_name')),
    beauty_full = model.objects.filter(approved=True).filter(category='beauty').exclude(city='').order_by('cat_ordering','city', 'business_name')
    beauty_blank = model.objects.filter(approved=True).filter(category='beauty').filter(city='').order_by('business_name')
    beauty = list(beauty_full) + list(beauty_blank)
    books_full = model.objects.filter(approved=True).filter(category='books').exclude(city='').order_by('cat_ordering','city', 'business_name')
    books_blank = model.objects.filter(approved=True).filter(category='books').filter(city='').order_by('business_name')
    books = list(books_full) + list(books_blank)
    cars_full = model.objects.filter(approved=True).filter(category='cars').exclude(city='').order_by('cat_ordering','city', 'business_name')
    cars_blank = model.objects.filter(approved=True).filter(category='cars').filter(city='').order_by('business_name')
    cars = list(cars_full) + list(cars_blank)
    child_full = model.objects.filter(approved=True).filter(category='child').exclude(city='').order_by('cat_ordering','city', 'business_name')
    child_blank = model.objects.filter(approved=True).filter(category='child').filter(city='').order_by('business_name')
    child = list(child_full) + list(child_blank)
    cleaning_full = model.objects.filter(approved=True).filter(category='cleaning').exclude(city='').order_by('cat_ordering','city', 'business_name')
    cleaning_blank = model.objects.filter(approved=True).filter(category='cleaning').filter(city='').order_by('business_name')
    cleaning = list(cleaning_full) + list(cleaning_blank)
    clothing_full = model.objects.filter(approved=True).filter(category='clothing').exclude(city='').order_by('cat_ordering','city', 'business_name')
    clothing_blank = model.objects.filter(approved=True).filter(category='clothing').filter(city='').order_by('business_name')
    clothing = list(clothing_full) + list(clothing_blank)
    construction_full = model.objects.filter(approved=True).filter(category='construction').exclude(city='').order_by('cat_ordering','city', 'business_name')
    construction_blank = model.objects.filter(approved=True).filter(category='construction').filter(city='').order_by('business_name')
    construction = list(construction_full) + list(construction_blank)
    education_full = model.objects.filter(approved=True).filter(category='education').exclude(city='').order_by('cat_ordering','city', 'business_name')
    education_blank = model.objects.filter(approved=True).filter(category='education').filter(city='').order_by('business_name')
    education = list(education_full) + list(education_blank)
    eldercare_full = model.objects.filter(approved=True).filter(category='eldercare').exclude(city='').order_by('cat_ordering','city', 'business_name')
    eldercare_blank = model.objects.filter(approved=True).filter(category='eldercare').filter(city='').order_by('business_name')
    eldercare = list(eldercare_full) + list(eldercare_blank)
    electronics_full = model.objects.filter(approved=True).filter(category='electronics').exclude(city='').order_by('cat_ordering','city', 'business_name')
    electronics_blank = model.objects.filter(approved=True).filter(category='electronics').filter(city='').order_by('business_name')
    electronics = list(electronics_full) + list(electronics_blank)
    entertainment_full = model.objects.filter(approved=True).filter(category='entertainment').exclude(city='').order_by('cat_ordering','city', 'business_name')
    entertainment_blank = model.objects.filter(approved=True).filter(category='entertainment').filter(city='').order_by('business_name')
    entertainment = list(entertainment_full) + list(entertainment_blank)
    farming_full = model.objects.filter(approved=True).filter(category='farming').exclude(city='').order_by('cat_ordering','city', 'business_name')
    farming_blank = model.objects.filter(approved=True).filter(category='farming').filter(city='').order_by('business_name')
    farming = list(farming_full) + list(farming_blank)
    florists_full = model.objects.filter(approved=True).filter(category='florists').exclude(city='').order_by('cat_ordering','city', 'business_name')
    florists_blank = model.objects.filter(approved=True).filter(category='florists').filter(city='').order_by('business_name')
    florists = list(florists_full) + list(florists_blank)
    grocery_full = model.objects.filter(approved=True).filter(category='grocery').exclude(city='').order_by('cat_ordering','city', 'business_name')
    grocery_blank = model.objects.filter(approved=True).filter(category='grocery').filter(city='').order_by('business_name')
    grocery = list(grocery_full) + list(grocery_blank)
    health_full = model.objects.filter(approved=True).filter(category='health').exclude(city='').order_by('cat_ordering','city', 'business_name')
    health_blank = model.objects.filter(approved=True).filter(category='health').filter(city='').order_by('business_name')
    health = list(health_full) + list(health_blank)
    home_full = model.objects.filter(approved=True).filter(category='home').exclude(city='').order_by('cat_ordering','city', 'business_name')
    home_blank = model.objects.filter(approved=True).filter(category='home').filter(city='').order_by('business_name')
    home = list(home_full) + list(home_blank)
    hotels_full = model.objects.filter(approved=True).filter(category='hotels').exclude(city='').order_by('cat_ordering','city', 'business_name')
    hotels_blank = model.objects.filter(approved=True).filter(category='hotels').filter(city='').order_by('business_name')
    hotels = list(hotels_full) + list(hotels_blank)
    jewelry_full = model.objects.filter(approved=True).filter(category='jewelry').exclude(city='').order_by('cat_ordering','city', 'business_name')
    jewelry_blank = model.objects.filter(approved=True).filter(category='jewelry').filter(city='').order_by('business_name')
    jewelry = list(jewelry_full) + list(jewelry_blank)
    legal_full = model.objects.filter(approved=True).filter(category='legal').exclude(city='').order_by('cat_ordering','city', 'business_name')
    legal_blank = model.objects.filter(approved=True).filter(category='legal').filter(city='').order_by('business_name')
    legal = list(legal_full) + list(legal_blank)
    lifestyle_full = model.objects.filter(approved=True).filter(category='lifestyle').exclude(city='').order_by('cat_ordering','city', 'business_name')
    lifestyle_blank = model.objects.filter(approved=True).filter(category='lifestyle').filter(city='').order_by('business_name')
    lifestyle = list(lifestyle_full) + list(lifestyle_blank)
    marketing_full = model.objects.filter(approved=True).filter(category='marketing').exclude(city='').order_by('cat_ordering','city', 'business_name')
    marketing_blank = model.objects.filter(approved=True).filter(category='marketing').filter(city='').order_by('business_name')
    marketing = list(marketing_full) + list(marketing_blank)
    medical_full = model.objects.filter(approved=True).filter(category='medical').exclude(city='').order_by('cat_ordering','city', 'business_name')
    medical_blank = model.objects.filter(approved=True).filter(category='medical').filter(city='').order_by('business_name')
    medical = list(medical_full) + list(medical_blank)
    other_full = model.objects.filter(approved=True).filter(category='other').exclude(city='').order_by('cat_ordering','city', 'business_name')
    other_blank = model.objects.filter(approved=True).filter(category='other').filter(city='').order_by('business_name')
    other = list(other_full) + list(other_blank)
    packaging_full = model.objects.filter(approved=True).filter(category='packaging').exclude(city='').order_by('cat_ordering','city', 'business_name')
    packaging_blank = model.objects.filter(approved=True).filter(category='packaging').filter(city='').order_by('business_name')
    packaging = list(packaging_full) + list(packaging_blank)
    pets_full = model.objects.filter(approved=True).filter(category='pets').exclude(city='').order_by('cat_ordering','city', 'business_name')
    pets_blank = model.objects.filter(approved=True).filter(category='pets').filter(city='').order_by('business_name')
    pets = list(pets_full) + list(pets_blank)
    photography_full = model.objects.filter(approved=True).filter(category='photography').exclude(city='').order_by('cat_ordering','city', 'business_name')
    photography_blank = model.objects.filter(approved=True).filter(category='photography').filter(city='').order_by('business_name')
    photography = list(photography_full) + list(photography_blank)
    professional_full = model.objects.filter(approved=True).filter(category='professional').exclude(city='').order_by('cat_ordering','city', 'business_name')
    professional_blank = model.objects.filter(approved=True).filter(category='professional').filter(city='').order_by('business_name')
    professional = list(professional_full) + list(professional_blank)
    realestate_full = model.objects.filter(approved=True).filter(category='real estate').exclude(city='').order_by('cat_ordering','city', 'business_name')
    realestate_blank = model.objects.filter(approved=True).filter(category='real estate').filter(city='').order_by('business_name')
    realestate = list(realestate_full) + list(realestate_blank)
    recreation_full = model.objects.filter(approved=True).filter(category='recreation').exclude(city='').order_by('cat_ordering','city', 'business_name')
    recreation_blank = model.objects.filter(approved=True).filter(category='recreation').filter(city='').order_by('business_name')
    recreation = list(recreation_full) + list(recreation_blank)
    restaurants_full = model.objects.filter(approved=True).filter(category='restaurants').exclude(city='').order_by('cat_ordering','city', 'business_name')
    restaurants_blank = model.objects.filter(approved=True).filter(category='restaurants').filter(city='').order_by('business_name')
    restaurants = list(restaurants_full) + list(restaurants_blank)
    security_full = model.objects.filter(approved=True).filter(category='security').exclude(city='').order_by('cat_ordering','city', 'business_name')
    security_blank = model.objects.filter(approved=True).filter(category='security').filter(city='').order_by('business_name')
    security = list(security_full) + list(security_blank)
    transportation_full = model.objects.filter(approved=True).filter(category='transportation').exclude(city='').order_by('cat_ordering','city', 'business_name')
    transportation_blank = model.objects.filter(approved=True).filter(category='transportation').filter(city='').order_by('business_name')
    transportation = list(transportation_full) + list(transportation_blank)
    visual_full = model.objects.filter(approved=True).filter(category='visual').exclude(city='').order_by('cat_ordering','city', 'business_name')
    visual_blank = model.objects.filter(approved=True).filter(category='visual').filter(city='').order_by('business_name')
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
    f = StateFilter(request.GET, queryset=model.objects.all())
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

def filterList(request):
    get = request.GET
    
    items = get.items()
    return HttpResponse(220)