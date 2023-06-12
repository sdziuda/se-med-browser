import os
from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit
import base64
import PyPDF2
from django.conf import settings

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
                request.session['phrase'] = phrase
                if phrase == '':
                    return render(request, 'index.html', {'search_form': form, 'search': True})

                context = {'search_form': form, 'search': True}
                med_list = get_med_list(phrase)
                top = request.session.get('top') or '25'
                if top == 'all':
                    context['med'] = med_list
                else:
                    context['med'] = med_list[:int(top)]
                context['top_form'] = TopForm(initial={'top': top})

                return render(request, 'index.html', context)

        elif request.POST.get('form_type') == 'top':
            phrase = request.POST.get('phrase') or ''
            top_form = TopForm(request.POST)

            if top_form.is_valid():
                top = top_form.cleaned_data['top']
                request.session['top'] = top
                search_form = SearchForm(initial={'phrase': phrase})
                context = {'search_form': search_form, 'search': True, 'top_form': top_form}

                med_list = get_med_list(phrase)
                if top == 'all':
                    context['med'] = med_list
                else:
                    context['med'] = med_list[:int(top)]
                return render(request, 'index.html', context)

        elif request.POST.get('form_type') == 'pdf':
            top = request.session.get('top') or '25'
            phrase = request.session.get('phrase')
            if phrase is None:
                context = {'search_form': SearchForm(), 'search': False}
            else:
                if top == 'all':
                    context = {'med': get_med_list(phrase)}
                else:
                    context = {'med': get_med_list(phrase)[:int(top)]}
                context['search'] = True
                context['search_form'] = SearchForm(initial={'phrase': phrase})
            context['top_form'] = TopForm(initial={'top': top})
            with open(os.path.join(settings.STATIC_ROOT, 'lupka.png'), 'rb') as f:
                context['search_png'] = base64.b64encode(f.read())
            with open(os.path.join(settings.STATIC_ROOT, 'pdf.png'), 'rb') as f:
                context['pdf_png'] = base64.b64encode(f.read())

            return html_to_pdf('pdf_template.html', context, request)

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
    med = med.union(Medicine.objects.filter(price__indication_range__icontains=phrase))
    med = med.union(Medicine.objects.filter(price__off_label_indication_range__icontains=phrase))
    med = med.order_by('name', 'form', 'dose', 'package_contents')

    med_list = [{'medicine': med_dict[m.GTIN_number], 'id': m_id % 2} for m_id, m in enumerate(med)]

    return med_list


def html_to_pdf(template_src, context_dict, request):
    template = get_template(template_src)
    html = template.render(context_dict)

    config = pdfkit.configuration(wkhtmltopdf='/app/bin/wkhtmltopdf')
    options = {
        'page-size': 'A4',
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0in',
        'margin-left': '0in',
        'encoding': 'UTF-8',
        'no-outline': None,
    }

    output = 'out_' + str(request.session.session_key) + '.pdf'
    output_no_last = 'out_no_last_' + str(request.session.session_key) + '.pdf'
    pdfkit.from_string(html, output, configuration=config, options=options)
    remove_last_page(output, output_no_last)
    with open(output_no_last, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="wyniki_wyszukiwania.pdf"'
        pdf.close()
    os.remove(output)
    os.remove(output_no_last)

    return response


def remove_last_page(input_path, output_path):
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)

        writer = PyPDF2.PdfWriter()
        if total_pages > 1:
            for page in reader.pages[:total_pages-1]:
                writer.add_page(page)
        else:
            writer.add_page(reader.pages[0])

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
