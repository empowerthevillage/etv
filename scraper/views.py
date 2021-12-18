from django.shortcuts import render
from bs4 import BeautifulSoup
from django.template.loader import render_to_string

def soup(request):
    page = render_to_string('georgia.html')
    soup = BeautifulSoup(page, 'html.parser')
    cells = soup.find_all(class_="_1Q9if")
    span = soup.span()
    context = {
        'cells': cells,
        'span': span
    }
    return render(request, 'scraper.html', context)


