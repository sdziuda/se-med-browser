from django.shortcuts import render
from django import forms
from .models import Medicine
from .globals import med_dict


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
                            widget=forms.Select(attrs={'onchange': 'topSubmit();'}))


def index(request):
    if request.method == 'POST':
        if request.POST.get('form_type') == 'search':
            form = SearchForm(request.POST)
            if form.is_valid():
                phrase = form.cleaned_data['phrase']
                if phrase == '':
                    return render(request, 'index.html', {'search_form': form, 'search': True})

                top_form = TopForm()
                med_list = get_med_list(phrase)

                context = {'search_form': form, 'search': True, 'top_form': top_form, 'med': med_list[:25]}
                return render(request, 'index.html', context)

        elif request.POST.get('form_type') == 'top':
            phrase = request.POST.get('phrase') or ''
            top_form = TopForm(request.POST)

            if top_form.is_valid():
                top = top_form.cleaned_data['top']
                search_form = SearchForm(initial={'phrase': phrase})
                context = {'search_form': search_form, 'search': True, 'top_form': top_form}

                med_list = get_med_list(phrase)
                if top == 'all':
                    context['med'] = med_list
                else:
                    context['med'] = med_list[:int(top)]
                return render(request, 'index.html', context)

    search_form = SearchForm()
    return render(request, 'index.html', {'search_form': search_form, 'search': False})


def get_med_list(phrase):
    if phrase == '':
        return []

    med = Medicine.objects.filter(name__icontains=phrase)
    med = med.union(Medicine.objects.filter(active_substance__name__icontains=phrase))
    med = med.union(Medicine.objects.filter(GTIN_number__icontains=phrase))
    med = med.union(Medicine.objects.filter(form__icontains=phrase))
    med = med.union(Medicine.objects.filter(dose__icontains=phrase))
    med = med.union(Medicine.objects.filter(package_contents__icontains=phrase))
    med = med.order_by('name', 'form', 'dose', 'package_contents')

    med_list = [{'medicine': med_dict[m.GTIN_number], 'id': m_id % 2} for m_id, m in enumerate(med)]

    return med_list