from django.shortcuts import render
from django import forms


class SearchForm(forms.Form):
    phrase = forms.CharField(max_length=2000,
                             label='',
                             widget=forms.TextInput(attrs={'placeholder': 'Wpisz wyszukiwaną frazę'}))


def index(request):
    if request.method == 'POST':
        if 'search.x' in request.POST:  # why 'search.x'? and why not 'search'? idk tbh, search doesn't work
            form = SearchForm(request.POST)
            if form.is_valid():
                phrase = form.cleaned_data['phrase']
                return render(request, 'index.html', {'phrase': phrase, 'search_form': form})

    search_form = SearchForm()
    return render(request, 'index.html', {'search_form': search_form})
