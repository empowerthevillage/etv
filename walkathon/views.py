from django.shortcuts import render, redirect
from .models import Walker, HomeGalleryImage

def walker_home(request):
    context = {
        'title': 'ETV 2023 Walkathon',
        'walkers': Walker.objects.all(),
        'photos': HomeGalleryImage.objects.all()
    }
    return render(request, 'walkathon_home.html', context)

def walker_detail(request, walker):
    try:
        walker_obj = Walker.objects.get(slug=walker)
        context = {
            'title': 'Support %s' %(walker_obj),
            'walker': walker_obj
        }
        return render(request, 'walker_detail.html', context)
    except:
        return redirect('/walkathon/')
    