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
