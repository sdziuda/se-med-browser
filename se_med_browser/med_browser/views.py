from django.shortcuts import render
from django import forms
from django.core.cache import cache
from .models import Medicine


class SearchForm(forms.Form):
    phrase = forms.CharField(max_length=2000,
                             label='',
                             widget=forms.TextInput(attrs={'placeholder': 'Wpisz wyszukiwaną frazę'}),
                             required=False)


class TopForm(forms.Form):
    top = forms.ChoiceField(choices=[(5, 5), (10, 10), (25, 25), (50, 50), (100, 100), ('all', 'Wszystkie')],
                            label='Pokaż',
                            initial=25,
                            required=False,
                            widget=forms.Select(attrs={'onchange': 'this.form.submit()'}))


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
                top_form = TopForm()
                cache.set('med', med)
                cache.set('phrase', phrase)
                return render(request, 'index.html', {'search_form': form, 'med': med[:25], 'search': True,
                                                      'top_form': top_form})
        elif 'top' in request.POST:
            med = cache.get('med')
            if med is None:
                med = []
            phrase = cache.get('phrase')
            if phrase is None:
                phrase = ''
            top_form = TopForm(request.POST)
            if top_form.is_valid():
                top = top_form.cleaned_data['top']
                search_form = SearchForm(initial={'phrase': phrase})
                context = {'search_form': search_form, 'search': True, 'top_form': top_form}
                if top == 'all':
                    context['med'] = med
                else:
                    context['med'] = med[:int(top)]
                return render(request, 'index.html', context)

    search_form = SearchForm()
    return render(request, 'index.html', {'search_form': search_form, 'search': False})

