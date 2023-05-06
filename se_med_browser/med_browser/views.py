from django.shortcuts import render
from django import forms
from .models import Medicine


class SearchForm(forms.Form):
    phrase = forms.CharField(max_length=2000,
                             label='',
                             widget=forms.TextInput(attrs={'placeholder': 'Wpisz wyszukiwaną frazę'}),
                             required=False)


def index(request):
    if request.method == 'POST':
        if 'search.x' in request.POST:  # why 'search.x'? and why not 'search'? idk tbh, search doesn't work
            form = SearchForm(request.POST)
            if form.is_valid():
                phrase = form.cleaned_data['phrase']
                if phrase == '':
                    return render(request, 'index.html', {'search_form': form, 'search': True})

                med = Medicine.objects.filter(name__icontains=phrase)
                med = med.union(Medicine.objects.filter(active_substance__name__icontains=phrase))
                med = med.union(Medicine.objects.filter(GTIN_number__icontains=phrase))
                med = med.union(Medicine.objects.filter(form__icontains=phrase))
                med = med.union(Medicine.objects.filter(dose__icontains=phrase))
                med = med.union(Medicine.objects.filter(package_contents__icontains=phrase))
                med = med.order_by('name', 'form', 'dose', 'package_contents')
                return render(request, 'index.html', {'search_form': form, 'med': med, 'search': True})

    search_form = SearchForm()
    return render(request, 'index.html', {'search_form': search_form, 'search': False})

