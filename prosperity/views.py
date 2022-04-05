from django.shortcuts import render

def economic_prosperity(request):
    context = {
        'title': 'ETV | Economic Prosperity & Employment',
    }
    return render(request, "prosperity.html", context)

def village_at_work(request):
    context = {
        'title': 'ETV | Village@Work',
    }
    return render(request, "village_at_work.html", context)
