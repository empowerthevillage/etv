from django.shortcuts import render
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
import json

from .models import VBPScraped
from tutorial.tutorial.spiders.quotes_spider import SBOSpider

def create_sbo_objects(request):
    json_data = open('scraper/templates/items.json')
    data = json.load(json_data)
    for x in data:
        obj, created = VBPScraped.objects.get_or_create(name=x['name'])
        obj.website = x['website']
        obj.phone = x['phones']
        obj.address = x['address']
        obj.category = x['category']
        obj.save()
    return HttpResponse('success')

def scraper(request):
    vbps = VBPScraped.objects.all()
    vbp_list = []
    for x in vbps:
        name = x.name
        address = str(x.address).split(",")
        if len(address) == 2:
            x.country, x.state = reversed(address)
        elif len(address) == 3:
            x.country, x.state, x.city = reversed(address)
            cityzip = x.city
            city_list = str(cityzip).split(" ")
            if len(city_list) == 1:
                x.city = city_list[0]
                x.zip = None
            elif len(city_list) == 2:
                if str(city_list[1]).isdecimal():
                    x.city = city_list[0]
                    x.zip = city_list[1]
                else:
                    x.city = cityzip
                    x.zip = None
            elif len(city_list) == 3:
                if str(city_list[2]).isdecimal():
                    x.zip = city_list[2]
                    x.city = ''.join(city_list.pop(2))
                    
                else:
                    x.city = cityzip
            elif len(city_list) == 4:
                if str(city_list[3]).isdecimal():
                    x.zip = city_list[3]
                    x.city = city_list.pop(3).join(" ")
                else:
                    x.city = cityzip
        elif len(address) == 4:
            x.country, x.state, cityzip, line2 = reversed(address) 
            city_list_base = cityzip.strip()
            city_list = city_list_base.split(' ')

            if len(city_list) == 1:
                x.city = city_list[0]
                x.zip = None
            elif len(city_list) == 2:
                if str(city_list[1]).isdecimal():
                    x.city = city_list[0]
                    x.zip = city_list[1]
                else:
                    x.city = cityzip
                    x.zip = None
            elif len(city_list) == 3:
                if str(city_list[2]).isdecimal():
                    x.zip = city_list[2]
                    x.city = city_list.pop(2).join(" ")
                else:
                    x.city = cityzip
            elif len(city_list) == 4:
                if str(city_list[3]).isdecimal():
                    x.zip = city_list[3]
                    x.city = city_list.pop(3).join(" ")
                else:
                    x.city = cityzip
        elif len(address) == 5:
            x.country, x.state, cityzip, line2, line1 = reversed(address) 
            city_list_base = cityzip.strip()
            city_list = str(city_list_base[0]).split(" ", maxsplit=1)

            if len(city_list) == 1:
                x.city = city_list[0]
                x.zip = None
            elif len(city_list) == 2:
                if str(city_list[1]).isdecimal():
                    x.city = city_list[0]
                    x.zip = city_list[1]
                else:
                    x.city = cityzip
                    x.zip = None
            elif len(city_list) == 3:
                if str(city_list[2]).isdecimal():
                    x.zip = city_list[2]
                    x.city = city_list.pop(2).join(" ")
                else:
                    x.city = cityzip
            elif len(city_list) == 4:
                if str(city_list[3]).isdecimal():
                    x.zip = city_list[3]
                    x.city = city_list.pop(3).join(" ")
                else:
                    x.city = cityzip
        x.save()
        print(x.city)
        
    context = {
        'vbp': VBPScraped.objects.all(),
    }
    return render(request, 'scraper.html', context)