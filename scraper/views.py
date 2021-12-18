from django.shortcuts import render
from bs4 import BeautifulSoup
from django.template.loader import render_to_string

def soup(request):
    page = render_to_string('ga-4.html')
    soup = BeautifulSoup(page, 'html.parser')
    cells = soup.find_all(class_="kn-detail-body")
    context = {
        'cells': cells,
    }
    return render(request, 'scraper.html', context)


