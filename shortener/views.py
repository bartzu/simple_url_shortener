from django.shortcuts import render

from .forms import FullURLForm


def shorten_url(request):
    form = FullURLForm()

    print(request.build_absolute_uri())

    if request.method == "POST":
        form = FullURLForm(request.POST)
        if form.is_valid():
            # place for all logic
            print("form submited correctly")

            # get or create long url

            # if there is a proposed shortcut
                # is it available?
                    # yes - create shortcut, redirect to success page

                    #no - add message and redirect to this view

            # create random sc, redirect to success page

    
    return render(request, 'shortener/shorten_url.html', {'form': form})