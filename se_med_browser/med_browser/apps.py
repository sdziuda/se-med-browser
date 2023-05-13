from django.apps import AppConfig
from .globals import med_dict


class MedBrowserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'med_browser'

    def ready(self):
        from .models import Medicine

        med = Medicine.objects.all()
        for m in med:
            med_dict[m.GTIN_number] = m.to_dict()
