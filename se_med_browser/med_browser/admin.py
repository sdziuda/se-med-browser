from django.contrib import admin
from .models import ActiveSubstance, Price, Medicine

# Register your models here.
admin.site.register(ActiveSubstance)
admin.site.register(Price)
admin.site.register(Medicine)
