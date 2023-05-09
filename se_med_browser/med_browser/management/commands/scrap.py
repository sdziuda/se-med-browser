import pandas as pd
import os
from django.core.management.base import BaseCommand
from med_browser.models import ActiveSubstance, Price, Medicine


def save_active_substance(name):
    active_substance_obj, created = ActiveSubstance.objects.get_or_create(name=name)
    if created:
        active_substance_obj.save()
    return active_substance_obj


def save_price(official_trade_price, indication_range, off_label_indication_range, payment_level,
               beneficiary_surcharge, medicine):
    price_obj, created = Price.objects.get_or_create(official_trade_price=official_trade_price,
                                                     indication_range=indication_range,
                                                     off_label_indication_range=off_label_indication_range,
                                                     payment_level=payment_level,
                                                     beneficiary_surcharge=beneficiary_surcharge,
                                                     medicine=medicine)
    if created:
        price_obj.save()
    return price_obj


def save_medicine(GTIN_number, sheet_nr, name, form, dose, package_contents, active_substance):
    medicine_obj, created = Medicine.objects.get_or_create(GTIN_number=GTIN_number,
                                                    sheet_nr=sheet_nr,
                                                    name=name,
                                                    form=form,
                                                    dose=dose,
                                                    package_contents=package_contents,
                                                    active_substance=active_substance,)
    if created:
        medicine_obj.save()
    return medicine_obj


def scraper():
    print(os.getcwd() + 'management/data.xlsx')
    file = os.getcwd() + '/med_browser/management/data.xlsx'

    for ind in range(1, 4):
        sheet_nr = 'A' + str(ind)
        df = pd.read_excel(file, sheet_name=sheet_nr, skiprows=1, header=0, index_col=0, dtype=str)
        i = 0

        for rec in df.values:
            print(f'{sheet_nr} {i}/{len(df.values)}')
            i += 1
            active_substance = rec[0]
            name = rec[1].split(',')[0]
            form = rec[1].split(',')[1]
            if len(rec[1].split(',')) > 2:
                dose = rec[1].split(',')[2]
            else:
                dose = 'nie dotyczy'
            package_contents = rec[2]
            GTIN_number = rec[3]
            official_trade_price = float(rec[7].replace(',', '.'))
            indication_range = rec[11]
            off_label_indication_range = rec[12]
            payment_level = rec[13]
            beneficiary_surcharge = float(rec[14].replace(',', '.'))

            active_substance_obj = save_active_substance(active_substance)
            medicine_obj = save_medicine(GTIN_number, sheet_nr, name, form, dose, package_contents,
                                         active_substance_obj)
            save_price(official_trade_price, indication_range, off_label_indication_range, payment_level,
                       beneficiary_surcharge, medicine_obj)

    for sheet_nr in ['B', 'C']:
        df = pd.read_excel(file, sheet_name=sheet_nr, skiprows=1, header=0, index_col=0, dtype=str)
        i = 0
        for rec in df.values:
            print(f'{sheet_nr} {i}/{len(df.values)}')
            i += 1
            active_substance = rec[0]
            name = rec[1].split(',')[0]
            form = rec[1].split(',')[1]
            if len(rec[1].split(',')) > 2:
                dose = rec[1].split(',')[2]
            else:
                dose = 'nie dotyczy'
            package_contents = rec[2]
            GTIN_number = rec[3]
            official_trade_price = float(rec[7].replace(',', '.'))
            indication_range = 'załącznik(i):\n' + rec[10]
            off_label_indication_range = ''
            payment_level = rec[11]
            beneficiary_surcharge = float(rec[12].replace(',', '.'))

            active_substance_obj = save_active_substance(active_substance)
            medicine_obj = save_medicine(GTIN_number, sheet_nr, name, form, dose, package_contents,
                                         active_substance_obj)
            save_price(official_trade_price, indication_range, off_label_indication_range, payment_level,
                       beneficiary_surcharge, medicine_obj)

    for sheet_nr in ['D', 'E']:
        df = pd.read_excel(file, sheet_name=sheet_nr, skiprows=1, header=0, index_col=0, dtype=str)
        i = 0
        for rec in df.values:
            print(f'{sheet_nr} {i}/{len(df.values)}')
            i += 1
            active_substance = rec[0]
            name = rec[1].split(',')[0]
            form = rec[1].split(',')[1]
            if len(rec[1].split(',')) > 2:
                dose = rec[1].split(',')[2]
            else:
                dose = 'nie dotyczy'
            package_contents = rec[2]
            GTIN_number = rec[3]
            price = Medicine.objects.filter(GTIN_number=GTIN_number, sheet_nr='A1')[0].price_set.all()[0]
            official_trade_price = price.official_trade_price
            indication_range = price.indication_range
            off_label_indication_range = price.off_label_indication_range
            if sheet_nr == 'D':
                payment_level = 'bezpłatny (senior)'
            else:
                payment_level = 'bezpłatny (ciężarna)'
            beneficiary_surcharge = float(0.0)

            active_substance_obj = save_active_substance(active_substance)
            medicine_obj = save_medicine(GTIN_number, sheet_nr, name, form, dose, package_contents,
                                         active_substance_obj)
            save_price(official_trade_price, indication_range, off_label_indication_range, payment_level,
                       beneficiary_surcharge, medicine_obj)


class Command(BaseCommand):
    help = 'Scrapes data from the excel file and saves it to the database'

    def handle(self, *args, **options):
        scraper()
