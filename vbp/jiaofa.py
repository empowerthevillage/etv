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