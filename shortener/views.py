from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .utils import url_within_domain, random_shortcut_value
from .models import FullURL, Shortcut
from .forms import FullURLForm


def shorten_url(request):
    form = FullURLForm()

    if request.method == "POST":
        form = FullURLForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            if url_within_domain(request, cd['full_url']):
                # do not allow shortening links from current domain
                message = "You can not shorten the shortener!"
                messages.error(request, message)

                return render(request, 'shortener/shorten_url.html', {'form': form})

            full_url, _ = FullURL.objects.get_or_create(url=cd['full_url'])
            if cd['proposed_shortcut']:
                try:
                    shortcut = Shortcut.objects.get(value=cd['proposed_shortcut'])
                    # shortcut already exists, get back to the view
                    message = "Shortcut you have chosen has alredy been used. \
                        Choose different one or leave the field empty to create random shortcut."                    
                    messages.error(request, message)
                    return render(request, 'shortener/shorten_url.html', {'form': form})

                except Shortcut.DoesNotExist:
                    shortcut = Shortcut.objects.create(value=cd['proposed_shortcut'], 
                        full_url=full_url)
                    
            else:
                # create shortcut with random value
                shortcut = Shortcut(value=random_shortcut_value(), full_url=full_url)
                shortcut.save()
            
            return HttpResponseRedirect(reverse('shortener:show_shortcut', args=(shortcut.value,)))

    
    return render(request, 'shortener/shorten_url.html', {'form': form})


def show_shortcut(request, shortcut_value):
    sc = get_object_or_404(Shortcut, value=shortcut_value)
    created_link = request.build_absolute_uri('/' + sc.value)

    context = {
        'created_link': created_link,
        'full_url': sc.full_url
    }

    return render(request, 'shortener/show_shortcut.html', context=context)


def redirect_to_url(request, shortcut):
    shortcut = get_object_or_404(Shortcut, value=shortcut)
    return HttpResponseRedirect(shortcut.full_url.url)