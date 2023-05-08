from django.db import models


class ActiveSubstance(models.Model):
    name = models.CharField(max_length=2000, primary_key=True)

    def __str__(self):
        return self.name


class Price(models.Model):
    official_trade_price = models.FloatField()
    indication_range = models.CharField(max_length=2000)
    off_label_indication_range = models.CharField(max_length=2000)
    payment_level = models.CharField(max_length=2000)
    beneficiary_surcharge = models.FloatField()

    def __str__(self):
        return str(self.official_trade_price)

    def to_dict(self):
        return {'official_trade_price': self.official_trade_price, 'indication_range': self.indication_range,
                'off_label_indication_range': self.off_label_indication_range, 'payment_level': self.payment_level,
                'beneficiary_surcharge': self.beneficiary_surcharge}


class Medicine(models.Model):
    GTIN_number = models.CharField(max_length=2000)
    sheet_nr = models.CharField(max_length=5)
    name = models.CharField(max_length=2000)
    form = models.CharField(max_length=2000)
    dose = models.CharField(max_length=2000)
    package_contents = models.CharField(max_length=2000)
    active_substance = models.ForeignKey(ActiveSubstance, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.PROTECT)

    def __str__(self):
        return self.name + ' ' + self.price.__str__() + ' ' + self.active_substance.__str__()

    def to_dict(self):
        return {'GTIN_number': self.GTIN_number, 'sheet_nr': self.sheet_nr, 'name': self.name, 'form': self.form,
                'dose': self.dose, 'package_contents': self.package_contents,
                'active_substance': self.active_substance.__str__(), 'price': self.price.to_dict()}
