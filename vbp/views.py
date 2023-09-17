import django
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.db.models import Q

from .models import mv_private, vbp_book, vbp_nj, vbp_ct, gift_guide, StateFilter, IndividualBook, vbp_ga, vbp_il, vbp_dc, vbp_md, vbp_mi, vbp_ny, vbp_nc, vbp_oh, vbp_pa, vbp_fl
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
            line = {"category": category, "verbose": str(verbose), "pagination": pagination_obj, "start_page": start_page, "last_page": page_count, "cover": "https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/vbp-%s-section-cover.webp" %(str(category)), "right": "https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/vbp-%s-section-right.webp" %(str(category)),"left": "https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/vbp-%s-section-left.webp" %(str(category))}
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
    return redirect('/events/')

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
  return render(request, 'vbp/nj_only.html')

def individual_state_view(request, slug):
  book_pairs = {
      'CT': vbp_ct,
      'GA': vbp_ga,
      'IL': vbp_il,
      'MD': vbp_md,
      'MI': vbp_mi,
      'NY': vbp_ny,
      'NJ': vbp_nj,
      'NC': vbp_nc,
      'OH': vbp_oh,
      'PA': vbp_pa,
      'DC': vbp_dc,
      'FL': vbp_fl,
    }
  try:
      book_obj = IndividualBook.objects.get(slug=slug)
      state = book_obj.state
      vbp_model = book_pairs[state]
      county_listings = vbp_model.objects.filter(approved=True)
      cats = []
      page_counter = 6
      for (category,verbose) in CATEGORY_CHOICES:
          listings = county_listings.filter(category=category)
          pages = Paginator(listings, 12)
          if len(listings)>0:
              cats.append({'category':category, 'verbose':verbose, 'pages':pages, 'start_page':page_counter,"cover": "https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/vbp-%s-section-cover.webp" %(category), "right": "https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/vbp-%s-section-right.webp" %(category),"left": "https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/vbp-%s-section-left.webp" %(category)})
              page_counter += pages.num_pages + 1
              
      n = int(len(cats)/2)
      m = n+1
      col1 = cats[0:n]
      col2 = cats[m:None]
      context = {
          'title': '%s Village Black Pages' %(book_obj.title),
          'cover_url': str(book_obj.cover_url),
          'sections': cats,
          'col1': col1,
          'col2': col2,
      }
      return render(request, 'vbp/county_only.html', context)
  except:
      return redirect('/village-black-pages/')
  
def individual_book_view(request, slug, state_slug):
    state_pairs = {
      'connecticut': 'CT',
      'georgia': 'GA',
      'illinois': 'IL',
      'maryland': 'MD',
      'michigan': 'MI',
      'new-york': 'NY',
      'new-jersey': 'NJ',
      'north-carolina': 'NC',
      'ohio': 'OH',
      'pennsylvania': 'PA',
      'dc': 'DC',
      'florida': 'FL',
    }
    book_pairs = {
      'CT': vbp_ct,
      'GA': vbp_ga,
      'IL': vbp_il,
      'MD': vbp_md,
      'MI': vbp_mi,
      'NY': vbp_ny,
      'NJ': vbp_nj,
      'NC': vbp_nc,
      'OH': vbp_oh,
      'PA': vbp_pa,
      'DC': vbp_dc,
      'FL': vbp_fl,
    }
    try:
      state_code = state_pairs[state_slug]
      book_obj = IndividualBook.objects.get(slug=slug, state=state_code)
      if book_obj.type == 'county':
          county = book_obj.title
          state = book_obj.state
          vbp_model = book_pairs[state]
          county_listings = vbp_model.objects.filter(county=county, approved=True)
          cats = []
          page_counter = 6
          for (category,verbose) in CATEGORY_CHOICES:
              listings = county_listings.filter(category=category)
              pages = Paginator(listings, 12)
              if len(listings)>0:
                  cats.append({'category':category, 'verbose':verbose, 'pages':pages, 'start_page':page_counter,"cover": "https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/vbp-%s-section-cover.webp" %(category), "right": "https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/vbp-%s-section-right.webp" %(category),"left": "https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/vbp-%s-section-left.webp" %(category)})
                  page_counter += pages.num_pages + 1
          n = int(len(cats)/2)
          m = n+1
          col1 = cats[0:n]
          col2 = cats[m:None]
          context = {
              'title': '%s Village Black Pages' %(book_obj.title),
              'cover_url': str(book_obj.cover_url),
              'sections': cats,
              'col1': col1,
              'col2': col2,
          }
          return render(request, 'vbp/county_only.html', context)
      else:
        return redirect('/village-black-pages/')
    except:
      return redirect('/village-black-pages/')
      
def essex_view(request):
    county_listings = vbp_nj.objects.filter(county="Essex County")
    cats = []
    page_counter = 6
    for (category,verbose) in CATEGORY_CHOICES:
        listings = county_listings.filter(category=category)
        pages = Paginator(listings, 12)
        if len(listings)>0:
            cats.append({'category':category, 'verbose':verbose, 'pages':pages, 'start_page':page_counter,"cover": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s.svg" %(str(verbose)), "right": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_right.svg" %(str(verbose)),"left": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_left.svg" %(str(verbose))})
            page_counter += pages.num_pages + 1
            
    n = int(len(cats)/2)
    m = n+1
    col1 = cats[0:n]
    col2 = cats[m:None]
    context = {
        'title': 'Essex County Village Black Pages',
        'cover_url': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/essex-cover.webp',
        'sections': cats,
        'col1': col1,
        'col2': col2,
    }
    return render(request, 'vbp/county_only.html', context)

def morris_view(request):
    county_listings = vbp_nj.objects.filter(county="Morris County")
    cats = []
    page_counter = 6
    for (category,verbose) in CATEGORY_CHOICES:
        listings = county_listings.filter(category=category)
        pages = Paginator(listings, 12)
        if len(listings)>0:
            cats.append({'category':category, 'verbose':verbose, 'pages':pages, 'start_page':page_counter,"cover": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s.svg" %(str(verbose)), "right": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_right.svg" %(str(verbose)),"left": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_left.svg" %(str(verbose))})
            page_counter += pages.num_pages + 1
            
    n = int(len(cats)/2)
    m = n+1
    col1 = cats[0:n]
    col2 = cats[m:None]
    context = {
        'title': 'Morris County Village Black Pages',
        'cover_url': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/morris-cover.webp',
        'sections': cats,
        'col1': col1,
        'col2': col2,
    }
    return render(request, 'vbp/county_only.html', context)
  
def montclair_view(request):
    county_listings = vbp_nj.objects.filter(Q(city='Montclair') | Q(city="Upper Montclair"))
    cats = []
    page_counter = 6
    for (category,verbose) in CATEGORY_CHOICES:
        listings = county_listings.filter(category=category)
        pages = Paginator(listings, 12)
        if len(listings)>0:
            cats.append({'category':category, 'verbose':verbose, 'pages':pages, 'start_page':page_counter,"cover": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s.svg" %(str(verbose)), "right": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_right.svg" %(str(verbose)),"left": "https://etv-empowerthevillage.s3.amazonaws.com/static/img/vbp/%s_left.svg" %(str(verbose))})
            page_counter += pages.num_pages + 1
            
    n = int(len(cats)/2)
    m = n+1
    col1 = cats[0:n]
    col2 = cats[m:None]
    context = {
        'title': 'Montclair Village Black Pages',
        'cover_url': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/montclair-min.jpg',
        'sections': cats,
        'col1': col1,
        'col2': col2,
    }
    return render(request, 'vbp/county_only.html', context)
  
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

def gift_guide_2_view(request):
    listings = gift_guide.objects.filter(approved=True)
    page1 = {
        'object_list': listings[0:2],
        'has_ads': True,
        'ads': [
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg7.webp',
                    'link': 'http://www.glassjarnaturalskin.com/',
                    'cols': 'col s7 offset-s1',
                    'after': '<div class="col s4"></div>'
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg14.webp',
                    'link': 'http://mentedcosmetics.com/',
                    'cols': 'col s7 offset-s4',
                }
            ],
    }
    page2 = {
        'object_list': listings[2:4],
        'has_ads': True,
        'ads': [
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg16.webp',
                    'link': 'https://www.sankofa.com/',
                    'cols': 'col s10 offset-s1',
                    'after': '<div class="col s1"></div>'
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/source-of-knowledge.webp',
                    'link': 'http://www.sourceofknowledgebookstore.com/',
                    'cols': 'col s10 offset-s1',
                },
            ],
    }
    page3 = {
        'object_list': listings[4:7],
        'has_ads': True,
        'ads': [
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg1.webp',
                    'link': 'https://www.ikuzidolls.com/',
                    'cols': 'col s4 offset-s1',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg17.webp',
                    'link': 'http://thebougiebabyboutique.com/',
                    'cols': 'col s7',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/chez-bebe.webp',
                    'link': 'https://chezbebeny.com/',
                    'cols': 'col s11 offset-s1',
                },
            ],
    }
    page4 = {
        'object_list': listings[7:13],
        'has_ads': True,
        'ads': [
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/baobab.webp',
                    'link': 'https://baobabclothing.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/indigo-style.webp',
                    'link': 'https://thecollectiveatindigostyle.com/shop',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/bk.webp',
                    'link': 'http://shop.thebkcircus.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/very-lovely-soles.webp',
                    'link': 'https://www.verylovelysoles.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg4.webp',
                    'link': 'https://shopemmalynlove.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/bonbont.webp',
                    'link': 'https://bonbontonline.com/',
                    'cols': 'col s4',
                }
            ],
    }
    page5 = {
        'object_list': listings[13:19],
        'has_ads': True,
        'ads': [
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/brandon-blackwell.webp',
                    'link': 'http://brandonblackwood.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/blacklove-boutique.webp',
                    'link': 'http://www.blackloveboutique.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/bluesole-shoes.webp',
                    'link': 'https://bluesoleshoes.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/sofistafunk.webp',
                    'link': 'https://sofistafunk.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg3.webp',
                    'link': 'https://lennoxandharvey.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg13.webp',
                    'link': 'http://www.sidelinebrand.com/',
                    'cols': 'col s4',
                },
            ],
    }
    page6 = {
        'object_list': listings[19:20],
        'has_ads': True,
        'ads': [
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/mtcflowers.webp',
                    'link': 'http://www.mtcflowers.com/',
                    'cols': 'col s10 offset-s1',
                },
            ],
    }
    page7 = {
        'object_list': listings[20:26],
        'has_ads': True,
        'ads': [
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg6.webp',
                    'link': 'https://www.teastorenj.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg8.webp',
                    'link': 'https://bazodee.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg12.webp',
                    'link': 'https://www.bse.coffee/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg7.webp',
                    'link': 'https://glassjarnaturaltea.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/harlem-choc.webp',
                    'link': 'https://harlemchocolatefactory.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/chip-bottle.webp',
                    'link': 'https://www.chipinabottle.com/shop-online/',
                    'cols': 'col s4',
                },
            ],
    }
    page8 = {
        'object_list': listings[26:29],
        'has_ads': True,
        'ads': [
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/zenfully.webp',
                    'link': 'https://zenfullymadecandleco.com/',
                    'cols': 'col s6',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg2.webp',
                    'link': 'https://theblackhome.com/',
                    'cols': 'col s6',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg9.webp',
                    'link': 'http://harlemcandlecompany.com/',
                    'cols': 'col s6 ml25',
                },
            ],
    }
    page9 = {
        'object_list': listings[29:31],
        'has_ads': True,
        'ads': [
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/awkwaaba.webp',
                    'link': 'https://www.akwaaba.com/',
                    'cols': 'col s8 offset-s2',
                },
            ],
    }
    page10 = {
        'object_list': listings[31:36],
        'has_ads': True,
        'ads': [
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg15.webp',
                    'link': 'http://www.maryshandsjewelry.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/gg5.webp',
                    'link': 'http://telfar.net/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/bonafide-glam.webp',
                    'link': 'https://bonafideglam.com/',
                    'cols': 'col s4',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/phila-diamond.webp',
                    'link': 'https://www.philadelphiadiamondco.com/',
                    'cols': 'col s5 ml29',
                },
                {
                    'src': 'https://pub-91c8b4fa01b34d9cb1fda46285f07f62.r2.dev/silk-tent.webp',
                    'link': 'https://www.thesilktent.com/',
                    'cols': 'col s5 ml5',
                },
            ],
    }
    pages = [page1, page2, page3, page4, page5, page6, page7, page8, page9, page10]
    
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
    return render(request, 'gift-guide-2.html', context)

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
                county = geocode_result.county
                print(county)
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


LINKS = [
  {
    "link": "https://14parishkitchen.com/",
    "sessions": 64
  },
  {
    "link": "https://issuu.com/empowerthevillage/docs/final_2021_annual_report?mode=window",
    "sessions": 56
  },
  {
    "link": "https://issuu.com/empowerthevillage/docs/tournament_information_3_",
    "sessions": 59
  },
  {
    "link": "https://www.facebook.com/Empower-The-Village-Nonprofit-Organization-105185814766521/",
    "sessions": 29
  },
  {
    "link": "https://www.instagram.com/empower_etv/",
    "sessions": 37
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-NJ-22.pdf?AWSAccessKeyId=AKIA6CEH7IPTHZENUK",
    "sessions": 26
  },
  {
    "link": "https://issuu.com/empowerthevillage/docs/etv_special_report_2020-2021_v2",
    "sessions": 18
  },
  {
    "link": "https://issuu.com/empowerthevillage/docs/press_release_empower_the_village_says_february_is?mode=win",
    "sessions": 15
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/obb-generic-2.jpg?AWSAccessKeyId=AKIA6CEH7IPTH",
    "sessions": 16
  },
  {
    "link": "https://youtu.be/ql8U8oy12wA",
    "sessions": 14
  },
  {
    "link": "https://baobabclothing.com/",
    "sessions": 11
  },
  {
    "link": "https://lennoxandharvey.com/",
    "sessions": 10
  },
  {
    "link": "https://www.youtube.com/channel/UCKMNMY8pqCId-PY4dCcKtaQ",
    "sessions": 27
  },
  {
    "link": "https://bazodee.com/",
    "sessions": 9
  },
  {
    "link": "http://telfar.net/",
    "sessions": 8
  },
  {
    "link": "http://www.maryshandsjewelry.com/",
    "sessions": 8
  },
  {
    "link": "https://goo.gl/maps/bnLBU2qJG81auBgg7",
    "sessions": 11
  },
  {
    "link": "https://shopemmalynlove.com/",
    "sessions": 8
  },
  {
    "link": "https://smile.amazon.com/ch/83-1330564",
    "sessions": 8
  },
  {
    "link": "https://theblackhome.com/",
    "sessions": 10
  },
  {
    "link": "https://www.facebook.com/Asahdas-Soulfood-Restaurant-104298064885687/",
    "sessions": 8
  },
  {
    "link": "http://brandonblackwood.com/",
    "sessions": 8
  },
  {
    "link": "http://www.sidelinebrand.com/",
    "sessions": 8
  },
  {
    "link": "http://www.sourceofknowledgebookstore.com/",
    "sessions": 7
  },
  {
    "link": "https://chezbebeny.com/",
    "sessions": 7
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/nj-22-print.pdf?AWSAccessKeyId=AKIA6CEH7IPTHZE",
    "sessions": 13
  },
  {
    "link": "https://www.sankofa.com/",
    "sessions": 7
  },
  {
    "link": "https://www.tapinto.net/towns/soma/articles/empower-the-village-celebrates-juneteenth-black-artists-",
    "sessions": 9
  },
  {
    "link": "http://www.glassjarnaturalskin.com/",
    "sessions": 6
  },
  {
    "link": "http://www.mtcflowers.com/",
    "sessions": 6
  },
  {
    "link": "https://twitter.com/empower_etv",
    "sessions": 6
  },
  {
    "link": "https://www.ikuzidolls.com/",
    "sessions": 7
  },
  {
    "link": "https://www.teastorenj.com/",
    "sessions": 6
  },
  {
    "link": "http://harlemcandlecompany.com/",
    "sessions": 6
  },
  {
    "link": "http://linkedin.com/company/empower-the-village",
    "sessions": 5
  },
  {
    "link": "http://mentedcosmetics.com/",
    "sessions": 5
  },
  {
    "link": "http://thebougiebabyboutique.com/",
    "sessions": 7
  },
  {
    "link": "https://www.bse.coffee/",
    "sessions": 5
  },
  {
    "link": "https://www.cleanjuice.com/",
    "sessions": 6
  },
  {
    "link": "https://www.devineplantery.com/",
    "sessions": 5
  },
  {
    "link": "https://www.sandissoulbites.com/",
    "sessions": 5
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-GA-22.pdf?AWSAccessKeyId=AKIA6CEH7IPTHZENUK",
    "sessions": 4
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-NJ-22-print.pdf?AWSAccessKeyId=AKIA6CEH7IPT",
    "sessions": 4
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-OH-2021.pdf?AWSAccessKeyId=AKIA6CEH7IPTHZEN",
    "sessions": 4
  },
  {
    "link": "https://issuu.com/empowerthevillage/docs/final_2021_annual_report_2_",
    "sessions": 6
  },
  {
    "link": "https://sofistafunk.com/",
    "sessions": 5
  },
  {
    "link": "https://www.gefkenflowers.net/",
    "sessions": 4
  },
  {
    "link": "https://www.willowandolivia.com/",
    "sessions": 5
  },
  {
    "link": "http://3stageschildcarecenter.com/",
    "sessions": 3
  },
  {
    "link": "http://anmlinstinct.com/",
    "sessions": 3
  },
  {
    "link": "http://popschickentogo.com/",
    "sessions": 3
  },
  {
    "link": "http://prudentia-grp.com/",
    "sessions": 3
  },
  {
    "link": "http://shop.thebkcircus.com/",
    "sessions": 3
  },
  {
    "link": "http://www.blackloveboutique.com/",
    "sessions": 3
  },
  {
    "link": "https://bonbontonline.com/",
    "sessions": 3
  },
  {
    "link": "https://certapro.com/morristown/",
    "sessions": 3
  },
  {
    "link": "https://cfnj.org/lindamurphy/",
    "sessions": 3
  },
  {
    "link": "https://cornbreadsoul.com/",
    "sessions": 3
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-NJ-2021.pdf?AWSAccessKeyId=AKIA6CEH7IPTHZEN",
    "sessions": 4
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-VA-2021.pdf?AWSAccessKeyId=AKIA6CEH7IPTHZEN",
    "sessions": 4
  },
  {
    "link": "https://goo.gl/maps/xQmezjMN8czG4eKj6",
    "sessions": 3
  },
  {
    "link": "https://issuu.com/empowerthevillage/docs/the_power_post_june_2021_issue",
    "sessions": 4
  },
  {
    "link": "https://issuu.com/empowerthevillage/docs/the_power_post_may_2021_inaugural_issue",
    "sessions": 3
  },
  {
    "link": "https://www.braintreegateway.com/merchants/tb3vd7jd2hynhxcn/verified",
    "sessions": 3
  },
  {
    "link": "https://www.diversityplus.com/",
    "sessions": 3
  },
  {
    "link": "https://www.facebook.com/A-Taste-Of-Royalty-LLC-2437980549788466/",
    "sessions": 3
  },
  {
    "link": "https://www.familyhealingcenternj.com/",
    "sessions": 3
  },
  {
    "link": "https://www.howdelishhd.com/",
    "sessions": 3
  },
  {
    "link": "https://www.janecartersolution.com/",
    "sessions": 5
  },
  {
    "link": "https://www.mopweezebakery.com/",
    "sessions": 3
  },
  {
    "link": "https://www.tapinto.net/towns/morristown/categories/press-releases/articles/empower-the-village-hono",
    "sessions": 4
  },
  {
    "link": "https://www.theteacompanycafe.com/",
    "sessions": 3
  },
  {
    "link": "https://www.wisengineering.com/",
    "sessions": 3
  },
  {
    "link": "http://alices-west-indian.edan.io/",
    "sessions": 2
  },
  {
    "link": "http://byteforbyte.net/",
    "sessions": 2
  },
  {
    "link": "http://cyclebar.com/location/livingston",
    "sessions": 2
  },
  {
    "link": "http://pinkluxurytoys.com/",
    "sessions": 2
  },
  {
    "link": "http://places.singleplatform.com/s--m-caribbean-cuisine/menu?ref=google",
    "sessions": 2
  },
  {
    "link": "http://sdesignset.com/",
    "sessions": 2
  },
  {
    "link": "http://www.athleticartsacademynj.com/",
    "sessions": 2
  },
  {
    "link": "http://www.atrstaffing.com/",
    "sessions": 2
  },
  {
    "link": "http://www.bgg-llc.com/",
    "sessions": 2
  },
  {
    "link": "http://www.blakesbeautypalace.com/",
    "sessions": 2
  },
  {
    "link": "http://www.diffvelopment.org/",
    "sessions": 2
  },
  {
    "link": "http://www.jaspice.com/",
    "sessions": 2
  },
  {
    "link": "http://www.masonfirmllc.com/",
    "sessions": 2
  },
  {
    "link": "http://www.michellegcameron.com/",
    "sessions": 2
  },
  {
    "link": "http://www.mitchelltitus.com/",
    "sessions": 2
  },
  {
    "link": "http://www.nrgcomics.com/",
    "sessions": 2
  },
  {
    "link": "http://www.tezroro.com/",
    "sessions": 2
  },
  {
    "link": "http://www.titleshotkennels.com/",
    "sessions": 2
  },
  {
    "link": "https://abbysconsulting.net/",
    "sessions": 2
  },
  {
    "link": "https://altechts.com/",
    "sessions": 2
  },
  {
    "link": "https://bluesoleshoes.com/",
    "sessions": 2
  },
  {
    "link": "https://diversityfoodbrands.com/",
    "sessions": 2
  },
  {
    "link": "https://edgartowndiner.com/",
    "sessions": 2
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-FL-2021.pdf?AWSAccessKeyId=AKIA6CEH7IPTHZEN",
    "sessions": 3
  },
  {
    "link": "https://firstclassofcolor.com/",
    "sessions": 2
  },
  {
    "link": "https://harlemchocolatefactory.com/",
    "sessions": 2
  },
  {
    "link": "https://jlexillc.com/",
    "sessions": 2
  },
  {
    "link": "https://joannewatkins.kw.com/",
    "sessions": 2
  },
  {
    "link": "https://joharionline.com/",
    "sessions": 2
  },
  {
    "link": "https://montclairdiner.com/",
    "sessions": 2
  },
  {
    "link": "https://nextdoor.com/pages/maleigha-marie-essentials-tinton-falls-nj/",
    "sessions": 2
  },
  {
    "link": "https://odabro-african-restaurant-lounge.business.site/",
    "sessions": 2
  },
  {
    "link": "https://shopcallmesparkle.com/",
    "sessions": 3
  },
  {
    "link": "https://sleemilaw.com/",
    "sessions": 2
  },
  {
    "link": "https://small-business-like-a-pro.thinkific.com/courses/how-did-i-get-here",
    "sessions": 2
  },
  {
    "link": "https://small-business-like-a-pro.thinkific.com/courses/overcome-your-fear-of-selling",
    "sessions": 5
  },
  {
    "link": "https://soulfoodlivingston.com/",
    "sessions": 2
  },
  {
    "link": "https://systahood.com/",
    "sessions": 2
  },
  {
    "link": "https://us02web.zoom.us/meeting/register/tZ0qc-mvqzgjEtX6q-qdVN6kHcXt-9IlWjNJ",
    "sessions": 2
  },
  {
    "link": "https://www.4chickscafeempanadas.com/",
    "sessions": 2
  },
  {
    "link": "https://www.akwaaba.com/akwaaba-at-buttonwood-manor/",
    "sessions": 2
  },
  {
    "link": "https://www.bctpartners.com/",
    "sessions": 2
  },
  {
    "link": "https://www.bledsoeinternational.com/",
    "sessions": 2
  },
  {
    "link": "https://www.cafemoso.com/",
    "sessions": 2
  },
  {
    "link": "https://www.charcutericatering.com/",
    "sessions": 2
  },
  {
    "link": "https://www.chefdeon.com/",
    "sessions": 2
  },
  {
    "link": "https://www.chipinabottle.com/shop-online/",
    "sessions": 2
  },
  {
    "link": "https://www.eimpactconsulting.com/",
    "sessions": 2
  },
  {
    "link": "https://www.elzarestaurant.com/",
    "sessions": 2
  },
  {
    "link": "https://www.facebook.com/CuppiedyCakes/",
    "sessions": 2
  },
  {
    "link": "https://www.facebook.com/GoldenKraftsShop/",
    "sessions": 2
  },
  {
    "link": "https://www.facebook.com/TPA1970",
    "sessions": 2
  },
  {
    "link": "https://www.facebook.com/Tasteysgailsouthernsoulfood",
    "sessions": 2
  },
  {
    "link": "https://www.facebook.com/hibiscus.restaurant.nj/",
    "sessions": 2
  },
  {
    "link": "https://www.facebook.com/royalte.slayz/",
    "sessions": 2
  },
  {
    "link": "https://www.goodworks4god.com/",
    "sessions": 2
  },
  {
    "link": "https://www.harperscafenj.com/",
    "sessions": 2
  },
  {
    "link": "https://www.heratij.com/pages/our-story",
    "sessions": 2
  },
  {
    "link": "https://www.home2skool.com/",
    "sessions": 2
  },
  {
    "link": "https://www.homesnap.com/Jennifer-DaSilva-1/gmb",
    "sessions": 3
  },
  {
    "link": "https://www.industrial-bank.com/",
    "sessions": 2
  },
  {
    "link": "https://www.instagram.com/blueberryvegancafe/?hl=en",
    "sessions": 2
  },
  {
    "link": "https://www.instagram.com/bradfordsbarrcatering/?hl=en",
    "sessions": 2
  },
  {
    "link": "https://www.instagram.com/colormecuteinsideandout/?hl=en",
    "sessions": 2
  },
  {
    "link": "https://www.jukejointsoulhouse.com/",
    "sessions": 2
  },
  {
    "link": "https://www.kumbahealth.com/",
    "sessions": 2
  },
  {
    "link": "https://www.loveandlonglaw.com/",
    "sessions": 2
  },
  {
    "link": "https://www.montclairbrewery.com/",
    "sessions": 2
  },
  {
    "link": "https://www.mvbiscuits.com/",
    "sessions": 2
  },
  {
    "link": "https://www.pimentogrill.biz/",
    "sessions": 2
  },
  {
    "link": "https://www.rentahelpermoving.com/",
    "sessions": 2
  },
  {
    "link": "https://www.tapinto.net/towns/denville/categories/press-releases/articles/empower-the-village-inc-an",
    "sessions": 3
  },
  {
    "link": "https://www.theglamemporium.com/?fbclid=IwAR1E_CLeoudun2dusSdcbvNnKi-fPLlR1jwulshadYk85i1oD-5kzLyASE",
    "sessions": 2
  },
  {
    "link": "https://www.thetrendyclutch.com/",
    "sessions": 2
  },
  {
    "link": "https://www.treasuresmade.com/",
    "sessions": 2
  },
  {
    "link": "https://www.womenwhowinnetwork.com/",
    "sessions": 2
  },
  {
    "link": "https://www.woulibamrestuarantnj.com/",
    "sessions": 2
  },
  {
    "link": "https://www.zenaestheticsspa.com/",
    "sessions": 2
  },
  {
    "link": "https://www.zmenu.com/jefferson-cafe-and-food-market-montclair-online-menu/",
    "sessions": 2
  },
  {
    "link": "https://www.zmenu.com/natural-start-east-orange-online-menu/",
    "sessions": 2
  },
  {
    "link": "tel:(862) 777-3193",
    "sessions": 2
  },
  {
    "link": "http://Jennifer.dasilva@compass.com/",
    "sessions": 1
  },
  {
    "link": "http://aaronallenmoving.com/",
    "sessions": 1
  },
  {
    "link": "http://amyruths.com/",
    "sessions": 1
  },
  {
    "link": "http://amzn.to/2QJxAve",
    "sessions": 1
  },
  {
    "link": "http://b2harlem.com/",
    "sessions": 1
  },
  {
    "link": "http://betterliferecovery.com/",
    "sessions": 1
  },
  {
    "link": "http://bitsycakes.godaddysites.com/",
    "sessions": 1
  },
  {
    "link": "http://bmwfhc10.wixsite.com/mysite-2",
    "sessions": 1
  },
  {
    "link": "http://cheapcarinsurancenewarknj.com/",
    "sessions": 1
  },
  {
    "link": "http://cmykolorgraphics.com/",
    "sessions": 1
  },
  {
    "link": "http://djs-digital.com/",
    "sessions": 1
  },
  {
    "link": "http://escapemts.com/",
    "sessions": 1
  },
  {
    "link": "http://hairbynedjetti.com/vnhop.htm",
    "sessions": 1
  },
  {
    "link": "http://hannahmonet.com/",
    "sessions": 1
  },
  {
    "link": "http://healinghandsmsg.com/",
    "sessions": 1
  },
  {
    "link": "http://healinghempreleaf.com/",
    "sessions": 1
  },
  {
    "link": "http://instagram.com/bloodsweatscienceAUTO",
    "sessions": 1
  },
  {
    "link": "http://is3sol.com/",
    "sessions": 1
  },
  {
    "link": "http://jjean-claude.com/",
    "sessions": 1
  },
  {
    "link": "http://johnsonlegalpc.com/",
    "sessions": 1
  },
  {
    "link": "http://jwbranding.co/",
    "sessions": 1
  },
  {
    "link": "http://komfort-zone.net/",
    "sessions": 1
  },
  {
    "link": "http://netpacintl.comm/",
    "sessions": 1
  },
  {
    "link": "http://reddz-bistro-grill.edan.io/",
    "sessions": 1
  },
  {
    "link": "http://sandrasnextgeneration.com/",
    "sessions": 1
  },
  {
    "link": "http://sandwichesunlimited.net/",
    "sessions": 1
  },
  {
    "link": "http://sbprou.com/",
    "sessions": 1
  },
  {
    "link": "http://shaescraftycorner.com/",
    "sessions": 1
  },
  {
    "link": "http://shellzthehookahchef.com/",
    "sessions": 1
  },
  {
    "link": "http://shopmymelanin.shop/",
    "sessions": 1
  },
  {
    "link": "http://smegsite.com/",
    "sessions": 1
  },
  {
    "link": "http://somlyfe.com/",
    "sessions": 1
  },
  {
    "link": "http://sunsplash.us/",
    "sessions": 1
  },
  {
    "link": "http://sylviasrestaurant.com/",
    "sessions": 1
  },
  {
    "link": "http://teesbetterbutters.com/",
    "sessions": 1
  },
  {
    "link": "http://thebkwgroup.com/",
    "sessions": 1
  },
  {
    "link": "http://tristatepropertydevelopers.com/",
    "sessions": 1
  },
  {
    "link": "http://ultrakosmic9.com/",
    "sessions": 1
  },
  {
    "link": "http://www.alishapean.com/",
    "sessions": 1
  },
  {
    "link": "http://www.allnaturalreset.com/",
    "sessions": 1
  },
  {
    "link": "http://www.amendabeauty.com/",
    "sessions": 1
  },
  {
    "link": "http://www.andersonpowerwash.com/",
    "sessions": 1
  },
  {
    "link": "http://www.angelabranch.com/",
    "sessions": 1
  },
  {
    "link": "http://www.aprettypennyfyt.com/",
    "sessions": 1
  },
  {
    "link": "http://www.ascent-group.com/",
    "sessions": 1
  },
  {
    "link": "http://www.ashehandmadedesigns.com/",
    "sessions": 1
  },
  {
    "link": "http://www.askmyhrguy.com/",
    "sessions": 1
  },
  {
    "link": "http://www.bakarr.com/",
    "sessions": 1
  },
  {
    "link": "http://www.blancblouse.com/",
    "sessions": 1
  },
  {
    "link": "http://www.bricks4kidz.com/essexcounty",
    "sessions": 1
  },
  {
    "link": "http://www.brosilybathandbody.com/",
    "sessions": 1
  },
  {
    "link": "http://www.brownsugarcollab.com/",
    "sessions": 1
  },
  {
    "link": "http://www.cjdfirstaidllc.com/",
    "sessions": 1
  },
  {
    "link": "http://www.cjkollective.com/",
    "sessions": 1
  },
  {
    "link": "http://www.cpacoombs.com/",
    "sessions": 1
  },
  {
    "link": "http://www.cynthiascaribbeanbakerynj.com/",
    "sessions": 1
  },
  {
    "link": "http://www.donebydbook.com/",
    "sessions": 1
  },
  {
    "link": "http://www.dontwaitcommunicate.com/",
    "sessions": 1
  },
  {
    "link": "http://www.dossagemassageandbodywork.com/",
    "sessions": 1
  },
  {
    "link": "http://www.dpc-books.com/home.html",
    "sessions": 1
  },
  {
    "link": "http://www.easttaylorinc.com/",
    "sessions": 1
  },
  {
    "link": "http://www.eliteitenterprisesolutions.com/",
    "sessions": 1
  },
  {
    "link": "http://www.enidbookscorp.com/",
    "sessions": 1
  },
  {
    "link": "http://www.estimescafe.com/",
    "sessions": 1
  },
  {
    "link": "http://www.excelsiorvas.com/",
    "sessions": 1
  },
  {
    "link": "http://www.faithinactioninc.com/",
    "sessions": 1
  },
  {
    "link": "http://www.familyfinancialmanagementpractice.com/",
    "sessions": 1
  },
  {
    "link": "http://www.freetownroadprojectnj.com/",
    "sessions": 1
  },
  {
    "link": "http://www.glowup395.com/",
    "sessions": 1
  },
  {
    "link": "http://www.highmaintenancehairco.com/",
    "sessions": 1
  },
  {
    "link": "http://www.hmhship.com/",
    "sessions": 1
  },
  {
    "link": "http://www.inkosicafe.com/",
    "sessions": 1
  },
  {
    "link": "http://www.instagram.com/TiffTheRealtor",
    "sessions": 1
  },
  {
    "link": "http://www.jacquiebirdspiritualwellness.com/",
    "sessions": 1
  },
  {
    "link": "http://www.jamagrille.com/",
    "sessions": 1
  },
  {
    "link": "http://www.lacyfoundation.org/",
    "sessions": 1
  },
  {
    "link": "http://www.liminscafe.com/",
    "sessions": 1
  },
  {
    "link": "http://www.morgan-contractors.com/",
    "sessions": 1
  },
  {
    "link": "http://www.natspinkcupcakes.com/",
    "sessions": 1
  },
  {
    "link": "http://www.nenrikitherapy.com/",
    "sessions": 1
  },
  {
    "link": "http://www.newarkspeaks2u.com/",
    "sessions": 1
  },
  {
    "link": "http://www.onestepaheadlearningcenter.com/",
    "sessions": 1
  },
  {
    "link": "http://www.partybusnewarknj.com/",
    "sessions": 1
  },
  {
    "link": "http://www.pocketbookhygieneshield.com/",
    "sessions": 1
  },
  {
    "link": "http://www.primeyourproperty.com/",
    "sessions": 1
  },
  {
    "link": "http://www.prisocklaw.com/",
    "sessions": 1
  },
  {
    "link": "http://www.realtalksessionseries.org/",
    "sessions": 1
  },
  {
    "link": "http://www.shaycosmetics.org/",
    "sessions": 1
  },
  {
    "link": "http://www.slayonbudgets.com/",
    "sessions": 1
  },
  {
    "link": "http://www.smittenkittenbeauty.com/",
    "sessions": 1
  },
  {
    "link": "http://www.sparklesweetkidsspa.com/",
    "sessions": 1
  },
  {
    "link": "http://www.stoneparkusa.com/",
    "sessions": 1
  },
  {
    "link": "http://www.sunrise-catering-unltd.com/",
    "sessions": 1
  },
  {
    "link": "http://www.sussexpressllc.com/",
    "sessions": 1
  },
  {
    "link": "http://www.thegirlyexperience.com/",
    "sessions": 1
  },
  {
    "link": "http://www.unitybrandhalal.com/",
    "sessions": 1
  },
  {
    "link": "http://www.urbanglobrand.com/",
    "sessions": 1
  },
  {
    "link": "http://www.valeriemorrisonphotography.com/",
    "sessions": 1
  },
  {
    "link": "http://www.waxandwonder.com/",
    "sessions": 1
  },
  {
    "link": "http://yallipop.wixsite.com/popjesus",
    "sessions": 1
  },
  {
    "link": "https://0.11.178.57/",
    "sessions": 1
  },
  {
    "link": "https://adamhelper.com/",
    "sessions": 1
  },
  {
    "link": "https://ahavafelicidad.wordpress.com/",
    "sessions": 1
  },
  {
    "link": "https://akuaba-fashions.business.site/",
    "sessions": 1
  },
  {
    "link": "https://alphaassembly.com/",
    "sessions": 1
  },
  {
    "link": "https://arrogantlyhumblebrand.com/",
    "sessions": 1
  },
  {
    "link": "https://atotalsolutioncpa.com/",
    "sessions": 1
  },
  {
    "link": "https://betterthanphilly.com/",
    "sessions": 1
  },
  {
    "link": "https://bffmakeupstudio.com/",
    "sessions": 1
  },
  {
    "link": "https://bombshellstudiosct.com/",
    "sessions": 1
  },
  {
    "link": "https://bonafideglam.com/",
    "sessions": 1
  },
  {
    "link": "https://breezycosmetics.com/",
    "sessions": 1
  },
  {
    "link": "https://brittneyscutsforkids.glossgenius.com/",
    "sessions": 2
  },
  {
    "link": "https://c-est-la-vie-oak-bluffs.edan.io/,",
    "sessions": 1
  },
  {
    "link": "https://cafemetronj.com/menu",
    "sessions": 1
  },
  {
    "link": "https://capitalicecream.com/",
    "sessions": 1
  },
  {
    "link": "https://carterfineartservices.com/",
    "sessions": 1
  },
  {
    "link": "https://chanelcreditsolutionsllc.com/",
    "sessions": 1
  },
  {
    "link": "https://devsjamaicancuisine.com/",
    "sessions": 1
  },
  {
    "link": "https://diasporaltd.com/",
    "sessions": 1
  },
  {
    "link": "https://donmullinsagency.com/",
    "sessions": 1
  },
  {
    "link": "https://dottiespetparlor.com/",
    "sessions": 1
  },
  {
    "link": "https://ecrservices.a-1sites.com/",
    "sessions": 1
  },
  {
    "link": "https://edtrust.org/wp-content/uploads/2014/09/Black-Degree-Attainment_FINAL.pdf",
    "sessions": 1
  },
  {
    "link": "https://elevenbyvenuswilliams.com/",
    "sessions": 1
  },
  {
    "link": "https://elitistcoffee.business.site/?utm_source=gmb&utm_medium=referral",
    "sessions": 1
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-AR-22.pdf?AWSAccessKeyId=AKIA6CEH7IPTHZENUK",
    "sessions": 1
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-AZ-22-print.pdf?AWSAccessKeyId=AKIA6CEH7IPT",
    "sessions": 1
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-AZ-22.pdf?AWSAccessKeyId=AKIA6CEH7IPTHZENUK",
    "sessions": 1
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-FL-22-print.pdf?AWSAccessKeyId=AKIA6CEH7IPT",
    "sessions": 1
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-NC-22-print.pdf?AWSAccessKeyId=AKIA6CEH7IPT",
    "sessions": 1
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-OH-22.pdf?AWSAccessKeyId=AKIA6CEH7IPTHZENUK",
    "sessions": 1
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/US-WI-22-print.pdf?AWSAccessKeyId=AKIA6CEH7IPT",
    "sessions": 1
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/nj-vote-22-min.jpg?AWSAccessKeyId=AKIA6CEH7IPT",
    "sessions": 1
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/obb-generic.jpeg?AWSAccessKeyId=AKIA6CEH7IPTHZ",
    "sessions": 1
  },
  {
    "link": "https://empowerthevillage.s3.amazonaws.com/static/img/obb-generic.jpg?AWSAccessKeyId=AKIA6CEH7IPTHZE",
    "sessions": 1
  },
  {
    "link": "https://etv-elift.s3.us-west-2.amazonaws.com/obb-ga.pdf",
    "sessions": 1
  },
  {
    "link": "https://fatus-kitchen.business.site/?utm_source=gmb&utm_medium=referral",
    "sessions": 1
  },
  {
    "link": "https://fitnessfastusa.com/",
    "sessions": 1
  },
  {
    "link": "https://goo.gl/maps/d4Sp5L5MyJiXtmSv9",
    "sessions": 1
  },
  {
    "link": "https://hlsjuicebarandgrill.com/",
    "sessions": 1
  },
  {
    "link": "https://homeawaychildcarecenter.com/",
    "sessions": 1
  },
  {
    "link": "https://hseymour.artspan.com/contact",
    "sessions": 1
  },
  {
    "link": "https://hunthamlinridley.com/",
    "sessions": 1
  },
  {
    "link": "https://instagram.com/hairraisingmv?igshid=YmMyMTA2M2Y=",
    "sessions": 1
  },
  {
    "link": "https://ipele.fitness/",
    "sessions": 1
  },
  {
    "link": "https://isayyessalonandspa.com/?fbclid=IwAR1hwa4buui_R-4aLmY29ntdW8VgsqiY2Yq9Yl6KjAa8pp-dpsyw6gw7ZfA",
    "sessions": 1
  },
  {
    "link": "https://issuu.com/empowerthevillage/docs/final_2021_annual_report_4_",
    "sessions": 1
  },
  {
    "link": "https://issuu.com/empowerthevillage/docs/the_power_post_june_2021_issue?mode=window",
    "sessions": 1
  },
  {
    "link": "https://itsteranga.com/",
    "sessions": 1
  },
  {
    "link": "https://jennelljones.com/",
    "sessions": 1
  },
  {
    "link": "https://justusbooks.com/",
    "sessions": 1
  },
  {
    "link": "https://kalimariwellness.com/",
    "sessions": 1
  },
  {
    "link": "https://karibecompany.com/",
    "sessions": 1
  },
  {
    "link": "https://kbbbqsmokehouse.com/",
    "sessions": 1
  },
  {
    "link": "https://kidcareconcierge.com/",
    "sessions": 1
  },
  {
    "link": "https://kidsincleats.org/",
    "sessions": 1
  },
  {
    "link": "https://knowhereart.com/",
    "sessions": 1
  },
  {
    "link": "https://kremeandkrumbs.com/",
    "sessions": 1
  },
  {
    "link": "https://kuumbamade.com/",
    "sessions": 1
  },
  {
    "link": "https://la-di.com/",
    "sessions": 1
  },
  {
    "link": "https://lagos-spot-nigerian-restaurant.business.site/",
    "sessions": 1
  },
  {
    "link": "https://laurenthestylist.net/",
    "sessions": 1
  },
  {
    "link": "https://leanbacksoulfood.com/",
    "sessions": 1
  },
  {
    "link": "https://lfcsupport.com/",
    "sessions": 1
  },
  {
    "link": "https://logropassaic.org/",
    "sessions": 1
  },
  {
    "link": "https://lovingarmsfoundation.org/",
    "sessions": 1
  },
  {
    "link": "https://m.facebook.com/Soul-Source-Counseling-105546724202673/",
    "sessions": 1
  },
  {
    "link": "https://maccakes.com/",
    "sessions": 1
  },
  {
    "link": "https://magiknsmellz.com/",
    "sessions": 1
  },
  {
    "link": "https://marksplaceaponline.com/order-now",
    "sessions": 1
  },
  {
    "link": "https://marshawoodruffe.kw.com/",
    "sessions": 1
  },
  {
    "link": "https://miraclebuttercream.com/",
    "sessions": 1
  },
  {
    "link": "https://mrhydeentertainment.wordpress.com/",
    "sessions": 1
  },
  {
    "link": "https://mvislandwiderealty.com/island-life-studio",
    "sessions": 1
  },
  {
    "link": "https://mwhitney.com/",
    "sessions": 1
  },
  {
    "link": "https://mybeautysite.com/vendor_shop/accessorizeyouhairboutique.html?fbclid=IwAR2tQsrUrFoU8NkJyiW6gP",
    "sessions": 1
  },
  {
    "link": "https://myonestoptaxes.com/Home/",
    "sessions": 1
  },
  {
    "link": "https://naijatechnews.com/",
    "sessions": 1
  },
  {
    "link": "https://napturalsbyreese.myshopify.com/",
    "sessions": 1
  },
  {
    "link": "https://newmethodrestoration.com/",
    "sessions": 1
  },
  {
    "link": "https://ninetwozero.square.site/",
    "sessions": 1
  },
  {
    "link": "https://oceanparkmv.com/realestate/agent/amy-goldson/",
    "sessions": 1
  },
  {
    "link": "https://owlabz.com/",
    "sessions": 1
  },
  {
    "link": "https://pitwebsite.com/",
    "sessions": 1
  },
  {
    "link": "https://qualicaremaids.wixsite.com/qualicare",
    "sessions": 1
  },
  {
    "link": "https://rccwsllc.com/",
    "sessions": 1
  },
  {
    "link": "https://recoverycenters.net/recovery-centers/new-jersey/sequoia-recovery/",
    "sessions": 1
  },
  {
    "link": "https://rhythmbrewingco.com/",
    "sessions": 1
  },
  {
    "link": "https://salaamicecreamparlor.business.site/",
    "sessions": 1
  },
  {
    "link": "https://santeresaw.com/",
    "sessions": 1
  },
  {
    "link": "https://saveurcreolerestaurant.com/",
    "sessions": 1
  },
  {
    "link": "https://sheimaginedsweets.com/",
    "sessions": 1
  },
  {
    "link": "https://silkwirejewelry.blogspot.com/",
    "sessions": 1
  },
  {
    "link": "https://simply-essence.com/",
    "sessions": 1
  },
  {
    "link": "https://sites.google.com/site/beautysecretshairandnails/?fbclid=IwAR13HOSVJvn_UQKGvu9dnSgT7sato6lSns",
    "sessions": 1
  },
  {
    "link": "https://small-business-like-a-pro.thinkific.com/courses/video-marketing-course",
    "sessions": 1
  },
  {
    "link": "https://somegoodfoodllc.com/",
    "sessions": 1
  },
  {
    "link": "https://southorangedentalcenter.com/",
    "sessions": 1
  },
  {
    "link": "https://spicenthing.com/",
    "sessions": 1
  },
  {
    "link": "https://static1.squarespace.com/static/5f539c4c68bd6f19d4743e52/t/60371d3945f2b47be0989dfa/161422469",
    "sessions": 1
  },
  {
    "link": "https://static1.squarespace.com/static/5f539c4c68bd6f19d4743e52/t/60784fec684d7f2b42043c23/161849751",
    "sessions": 1
  },
  {
    "link": "https://superarstrike.com/",
    "sessions": 1
  },
  {
    "link": "https://sweetgirldesserts.squarespace.com/",
    "sessions": 1
  },
  {
    "link": "https://technologyconcepts.com/",
    "sessions": 1
  },
  {
    "link": "https://tendernessherbsandteas.com/",
    "sessions": 1
  },
  {
    "link": "https://thecollectiveatindigostyle.com/shop",
    "sessions": 1
  },
  {
    "link": "https://thedancingblender.com/",
    "sessions": 1
  },
  {
    "link": "https://thesdbfirm.com/",
    "sessions": 1
  },
  {
    "link": "https://tonniesminis.com/",
    "sessions": 1
  },
  {
    "link": "https://unapologetically-healthy-llc.myshopify.com/",
    "sessions": 1
  },
  {
    "link": "https://urbantastenj.com/",
    "sessions": 1
  },
  {
    "link": "https://vector-international.com/",
    "sessions": 1
  },
  {
    "link": "https://worldofkitt.com/",
    "sessions": 1
  },
  {
    "link": "https://www.1blossom2bloom.com/",
    "sessions": 1
  },
  {
    "link": "https://www.4brothersbreakfasts.com/",
    "sessions": 1
  },
  {
    "link": "https://www.aboveartstudios.com/",
    "sessions": 1
  },
  {
    "link": "https://www.afrotaco.com/",
    "sessions": 1
  },
  {
    "link": "https://www.akwaaba.com/",
    "sessions": 1
  },
  {
    "link": "https://www.alliebscozykitchen.com/",
    "sessions": 1
  },
  {
    "link": "https://www.allmenus.com/nj/jersey-city/59019-vip-diner-restaurant/menu/",
    "sessions": 1
  },
  {
    "link": "https://www.alveyseducationprograms.com/",
    "sessions": 1
  },
  {
    "link": "https://www.annieleegifts.com/",
    "sessions": 1
  },
  {
    "link": "https://www.bedelinevents.com/home.html",
    "sessions": 1
  },
  {
    "link": "https://www.bedroomkandi.com/11967",
    "sessions": 1
  },
  {
    "link": "https://www.bellanaillounge.com/",
    "sessions": 1
  },
  {
    "link": "https://www.bestinclasseducation.com/",
    "sessions": 1
  },
  {
    "link": "https://www.bethdianasmith.com/",
    "sessions": 1
  },
  {
    "link": "https://www.bettyleejeans.com/",
    "sessions": 1
  },
  {
    "link": "https://www.bevskakekafe.com/",
    "sessions": 1
  },
  {
    "link": "https://www.blazetherapeutics.com/",
    "sessions": 1
  },
  {
    "link": "https://www.blueprintcafelounge.com/",
    "sessions": 1
  },
  {
    "link": "https://www.bluewellnesscenter.com/",
    "sessions": 1
  },
  {
    "link": "https://www.bodygarbagehandmade.com/",
    "sessions": 1
  },
  {
    "link": "https://www.burnettplasticsurgery.com/?utm_source=GMB&utm_medium=organic&utm_campaign=westfield",
    "sessions": 1
  },
  {
    "link": "https://www.cafemobaynj.com/",
    "sessions": 1
  },
  {
    "link": "https://www.caleensdayspa.com/",
    "sessions": 1
  },
  {
    "link": "https://www.capecodlobsterrolls.com/",
    "sessions": 1
  },
  {
    "link": "https://www.chaotickoko.com/",
    "sessions": 1
  },
  {
    "link": "https://www.charlesmovingandstorage.com/",
    "sessions": 1
  },
  {
    "link": "https://www.chocolatharlem.com/",
    "sessions": 1
  },
  {
    "link": "https://www.compass.com/agents/jennifer-daSilva/?referrer=omnibox",
    "sessions": 1
  },
  {
    "link": "https://www.coraltours.org/",
    "sessions": 1
  },
  {
    "link": "https://www.cousenrose.com/'",
    "sessions": 1
  },
  {
    "link": "https://www.crockettsfishfry.com/",
    "sessions": 1
  },
  {
    "link": "https://www.cudgelworks.comm/",
    "sessions": 1
  },
  {
    "link": "https://www.culturedexpressions.com/",
    "sessions": 1
  },
  {
    "link": "https://www.culturenailbar.com/",
    "sessions": 1
  },
  {
    "link": "https://www.dandtllc.com/",
    "sessions": 1
  },
  {
    "link": "https://www.davrontours.com/",
    "sessions": 1
  },
  {
    "link": "https://www.dcenewark.com/",
    "sessions": 1
  },
  {
    "link": "https://www.deardiaryinfo.org/",
    "sessions": 1
  },
  {
    "link": "https://www.digitalwebsitedevelopment.com/",
    "sessions": 2
  },
  {
    "link": "https://www.dillystaqueria.com/",
    "sessions": 2
  },
  {
    "link": "https://www.diorsbeautylounge.com/",
    "sessions": 1
  },
  {
    "link": "https://www.diversant.com/",
    "sessions": 1
  },
  {
    "link": "https://www.dsslaw.com/",
    "sessions": 1
  },
  {
    "link": "https://www.enginfotech.com/",
    "sessions": 1
  },
  {
    "link": "https://www.enjoyinglifefully.com/",
    "sessions": 1
  },
  {
    "link": "https://www.etsy.com/shop/CreativeStitchNDiva",
    "sessions": 1
  },
  {
    "link": "https://www.events.sankofa.com/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/2527cleaning/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/2muchsaucefoodtruck/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/Brick-Church-Pharmacy-103791134759103/reviews/?ref=page_internal",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/CaribbeanTouchMontclair/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/Carlis-Lounge-156093037761593/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/DandJcooking/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/DocsWaffleHouse/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/EdibleArtOfNewton/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/GOFSLLC//",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/Haitiancaribbeancuisine/about/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/HeadrestBarber",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/Jimmy-Has-It-Covered-358670644327013/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/JustJEUT/?ref=py_c&__xts__=-R",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/MadamsBeautySupply/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/NewarkBlackstone/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/SoCoCafenj/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/allN1BeautySupply/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/alonyavirtualvintage/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/cestlaviemv/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/cjbakerco",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/cksavoryscents/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/cryoutcave",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/ebonenviro/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/goodkarmaentinc/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/legenDerrygr88ness/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/levelonebakery/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/liteandsouleatery",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/mosalloccasioncateringllc/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/motherknows.org",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/pages/Nu%20Style%20Hair%20Cut%20Creators/134404429973102/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/pages/category/Day-Spa/Francines-Salon-Day-Spa-111561928885294/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/pages/category/Family-Style-Restaurant/Elmas-Kitchen-1564581303787359/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/pages/category/Grocery-Store/Lulus-Ice-Cream-Cafe-105263537493071/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/pages/category/Jamaican-Restaurant/Vineyard-Caribbean-Cuisine-2729748265140",
    "sessions": 2
  },
  {
    "link": "https://www.facebook.com/pages/category/Product-Service/Rashine-Divine-Dream-Cuisine-361392211026072",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/pages/category/Seafood-Restaurant/IM-FISH-N-GRILL-474681939388010/",
    "sessions": 1
  },
  {
    "link": "https://www.facebook.com/thelightdome/",
    "sessions": 1
  },
  {
    "link": "https://www.flavorsmvy.com/",
    "sessions": 1
  },
  {
    "link": "https://www.forsythseafood.com/home/",
    "sessions": 1
  },
  {
    "link": "https://www.freetownkitchen.com/menu",
    "sessions": 1
  },
  {
    "link": "https://www.fritaille.com/",
    "sessions": 1
  },
  {
    "link": "https://www.funkyphotoboothsandvideo.com/",
    "sessions": 1
  },
  {
    "link": "https://www.fuzeddining.life/",
    "sessions": 1
  },
  {
    "link": "https://www.geekschip.com/services/digital-marketing-services-in-hyderabad.html",
    "sessions": 1
  },
  {
    "link": "https://www.glamourgripsbynellie.com/?fbclid=IwAR0zes-RNKAdsPIM6MhlbxiomM6MgJQ9xmLJer7xuN43xEixXhktm",
    "sessions": 1
  },
  {
    "link": "https://www.google.com/url?q=https://brittneyscutsforkids.glossgenius.com/?fbclid%3DIwAR3HFVfvByRGtB",
    "sessions": 1
  },
  {
    "link": "https://www.google.com/url?q=https://freehaveneducationalfarms.com/&sa=D&ust=1607884075452000&usg=AF",
    "sessions": 1
  },
  {
    "link": "https://www.google.com/url?q=https://www.tinapearsonsalon.com/&sa=D&ust=1607884075455000&usg=AFQjCNG",
    "sessions": 1
  },
  {
    "link": "https://www.grubhub.com/restaurant/eatwell-african-cuisine-36-union-ave-irvington/2217405",
    "sessions": 1
  },
  {
    "link": "https://www.grubhub.com/restaurant/erics-jamaican-cuisine-309-main-st-boonton/1506452",
    "sessions": 1
  },
  {
    "link": "https://www.grubhub.com/restaurant/michelle-caribbean-american-cuisine-730-chancellor-avenue-irvingt",
    "sessions": 1
  },
  {
    "link": "https://www.grubhub.com/restaurant/sonia-classic-caribbean-restaurant-449-william-street-east-orange",
    "sessions": 1
  },
  {
    "link": "https://www.grubhub.com/restaurant/yardy-real-jamaican-food-1326-atlantic-ave-atlantic-city/1190838",
    "sessions": 1
  },
  {
    "link": "https://www.haircoutureboutique.com/",
    "sessions": 1
  },
  {
    "link": "https://www.hardworknoexcuses.com/",
    "sessions": 1
  },
  {
    "link": "https://www.healthgrades.com/physician/dr-rudolph-willis-ytl73",
    "sessions": 1
  },
  {
    "link": "https://www.hillerystreetgrill.net/",
    "sessions": 1
  },
  {
    "link": "https://www.honeyandvinylmusic.com/?utm_campaign=PartySlate&utm_medium=referral&utm_source=partyslat",
    "sessions": 1
  },
  {
    "link": "https://www.honeydippednaildesigns.com/",
    "sessions": 1
  },
  {
    "link": "https://www.ihop.com/en/restaurants-irvington-nj/1212-springfield-ave-2055",
    "sessions": 1
  },
  {
    "link": "https://www.imperialacq.com/",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/beautyadourned/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/bonfunwine/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/cheesecakesbydiamond/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/conphidentmusic/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/crystalsista/",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/deedeejerrys_sweettreats/",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/foreveraudacious/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/greatfcknfood/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/harlynn.harris_productions/",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/irvinjprod/?hl=en",
    "sessions": 2
  },
  {
    "link": "https://www.instagram.com/kaystayslayed/",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/kreationsbykay__/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/loverosecouture/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/nzurigold/",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/steakntake1/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/stikz_cigars/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/taste_of_flava/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.instagram.com/wingz_r_us/?hl=en",
    "sessions": 1
  },
  {
    "link": "https://www.jameshhunt.com/",
    "sessions": 1
  },
  {
    "link": "https://www.jerelwashington.com/",
    "sessions": 1
  },
  {
    "link": "https://www.jnfsteam.com/",
    "sessions": 1
  },
  {
    "link": "https://www.joyfullzone.com/",
    "sessions": 1
  },
  {
    "link": "https://www.jusbnaturl.com/",
    "sessions": 1
  },
  {
    "link": "https://www.kheperasbluelotus.com/",
    "sessions": 1
  },
  {
    "link": "https://www.kinfolkfamilyhealth.com/",
    "sessions": 1
  },
  {
    "link": "https://www.kizkopop.com/",
    "sessions": 1
  },
  {
    "link": "https://www.labelleartgallery.com/",
    "sessions": 1
  },
  {
    "link": "https://www.linkedin.com/in/corriner/",
    "sessions": 1
  },
  {
    "link": "https://www.linkedin.com/in/daryl-scales-ii-928aa0a8/",
    "sessions": 1
  },
  {
    "link": "https://www.lisascott.org/",
    "sessions": 1
  },
  {
    "link": "https://www.luken.nyc/",
    "sessions": 1
  },
  {
    "link": "https://www.maids.com/44/?utm_source=GMB_listing&utm_medium=organic",
    "sessions": 1
  },
  {
    "link": "https://www.maisonharlem.com/",
    "sessions": 1
  },
  {
    "link": "https://www.masseyagency.com/",
    "sessions": 1
  },
  {
    "link": "https://www.mesobrestaurant.com/",
    "sessions": 1
  },
  {
    "link": "https://www.mlcplus.com/",
    "sessions": 1
  },
  {
    "link": "https://www.ndbh.com/",
    "sessions": 1
  },
  {
    "link": "https://www.nettarius.com/",
    "sessions": 1
  },
  {
    "link": "https://www.nkboston.com/",
    "sessions": 1
  },
  {
    "link": "https://www.off-thehanger.com/",
    "sessions": 1
  },
  {
    "link": "https://www.ordercrabbae.com/",
    "sessions": 1
  },
  {
    "link": "https://www.philadelphiadiamondco.com/",
    "sessions": 1
  },
  {
    "link": "https://www.preciousbartending.com/",
    "sessions": 1
  },
  {
    "link": "https://www.primelinepackaging.com/",
    "sessions": 1
  },
  {
    "link": "https://www.productjunkienaturals.com/",
    "sessions": 1
  },
  {
    "link": "https://www.purelovepies.com/",
    "sessions": 1
  },
  {
    "link": "https://www.reidfinancialsolutions.com/",
    "sessions": 1
  },
  {
    "link": "https://www.sarrahcafenj.com/",
    "sessions": 1
  },
  {
    "link": "https://www.seamless.com/menu/plainfield-best-in-town-225-garfield-ave-plainfield/1028710",
    "sessions": 1
  },
  {
    "link": "https://www.sequoiarecovery.com/locations/Hoboken/",
    "sessions": 1
  },
  {
    "link": "https://www.serenityskincare.com/",
    "sessions": 1
  },
  {
    "link": "https://www.sharmturals.com/",
    "sessions": 1
  },
  {
    "link": "https://www.shopefb.com/",
    "sessions": 1
  },
  {
    "link": "https://www.skipfinley.com/",
    "sessions": 1
  },
  {
    "link": "https://www.smapa.org/",
    "sessions": 1
  },
  {
    "link": "https://www.smartsparkmedia.com/",
    "sessions": 1
  },
  {
    "link": "https://www.soulfoodfactory.com/",
    "sessions": 1
  },
  {
    "link": "https://www.stellarsmilecenter.com/",
    "sessions": 1
  },
  {
    "link": "https://www.stephenreidphotography.com/",
    "sessions": 1
  },
  {
    "link": "https://www.sweetsavorypalmers.com/",
    "sessions": 1
  },
  {
    "link": "https://www.symphonystreasures.com/",
    "sessions": 1
  },
  {
    "link": "https://www.tasteofthetriad.com/about",
    "sessions": 1
  },
  {
    "link": "https://www.thecafemetro.com/",
    "sessions": 2
  },
  {
    "link": "https://www.thedynasmiles.com/",
    "sessions": 1
  },
  {
    "link": "https://www.thelittlebohobookshop.com/",
    "sessions": 1
  },
  {
    "link": "https://www.therailsidecafe.com/",
    "sessions": 1
  },
  {
    "link": "https://www.thesilktent.com/",
    "sessions": 1
  },
  {
    "link": "https://www.thewalla.com/",
    "sessions": 1
  },
  {
    "link": "https://www.theyoniconnection.com/",
    "sessions": 1
  },
  {
    "link": "https://www.topknotchsoultrydelights.com/",
    "sessions": 1
  },
  {
    "link": "https://www.toptastecaribbean.com/online-ordering",
    "sessions": 1
  },
  {
    "link": "https://www.tvisha.com/services/mobile-app-development-company-maintenance-support-android-ios.html",
    "sessions": 1
  },
  {
    "link": "https://www.twofishfiveloaves.com/",
    "sessions": 1
  },
  {
    "link": "https://www.urbanairtrampolinepark.com/locations/new-jersey/south-hackensack",
    "sessions": 1
  },
  {
    "link": "https://www.verylovelysoles.com/",
    "sessions": 1
  },
  {
    "link": "https://www.waterworkslaundry.com/",
    "sessions": 1
  },
  {
    "link": "https://www.watsonrice.com/",
    "sessions": 1
  },
  {
    "link": "https://www.wearejerseyent.com/",
    "sessions": 1
  },
  {
    "link": "https://www.winstonskitchenmv.com/menu",
    "sessions": 1
  },
  {
    "link": "https://www.wwshippingco.com/",
    "sessions": 1
  },
  {
    "link": "https://www.ycinvited.com/",
    "sessions": 1
  },
  {
    "link": "https://www.yelp.com/biz/gealie-family-eatery-east-orange",
    "sessions": 1
  },
  {
    "link": "https://www.yelp.com/biz/j-and-j-caribbean-restaurant-maplewood",
    "sessions": 1
  },
  {
    "link": "https://www.yelp.com/biz/js-southern-style-cafe-city-of-orange",
    "sessions": 1
  },
  {
    "link": "https://www.yelp.com/biz/marckys-restaurant-irvington-3",
    "sessions": 2
  },
  {
    "link": "https://www.yelp.com/biz/stage-5-restaurant-and-grill-east-orange",
    "sessions": 1
  },
  {
    "link": "https://www.yelp.com/biz/surulere-suya-spot-union",
    "sessions": 1
  },
  {
    "link": "https://www.zenitheventspace.com/",
    "sessions": 1
  },
  {
    "link": "https://www.zmenu.com/zesty-wings-and-tasty-things-east-orange-online-menu/",
    "sessions": 1
  },
  {
    "link": "https://yourdesignpartner.com/",
    "sessions": 1
  },
  {
    "link": "https://yourvacationresorts.com/home/",
    "sessions": 1
  },
  {
    "link": "https://zenfullymadecandleco.com/",
    "sessions": 1
  },
  {
    "link": "instagram: @NyamnzMV",
    "sessions": 1
  },
  {
    "link": "instagram:@genosbackyardbbq",
    "sessions": 1
  },
  {
    "link": "mailto:%20info@empowerthevillage.org",
    "sessions": 1
  },
  {
    "link": "mailto:info@empowerthevillage.org",
    "sessions": 1
  },
  {
    "link": "tel:(917) 566-5900",
    "sessions": 1
  },
  {
    "link": "http://sagetitle.com/",
    "sessions": 1
  }
]

from .models import vbp_va

def analytics(request):
    links = LINKS
    businesses = []
    for x in links:
        try:
            qs = vbp_va.objects.filter(website__contains=x["link"])
            if len(qs) > 0:
                businesses.append({'business': str(qs.first()), 'category': str(qs.first().category)})
        except:
            pass
    return JsonResponse(businesses, safe=False)