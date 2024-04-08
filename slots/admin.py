from django.contrib import admin

from slots.models import Service, MasterSchedule, Booking

# Register your models here.
admin.site.register(Service)
admin.site.register(MasterSchedule)
admin.site.register(Booking)
