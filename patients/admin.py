from django.contrib import admin

from .models import Patient, Counsellor, Appointment

# Register your models here.
admin.site.register(Patient)
admin.site.register(Counsellor)
admin.site.register(Appointment)
