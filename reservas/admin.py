from calendar import Calendar
from django.contrib import admin
from .models import gallery, meetingRoomCalendar, mensagens, Product, reservas_Coworking, reservas_Coworking_provisoria, Price, Wallet


admin.site.register(mensagens)
admin.site.register(meetingRoomCalendar)
admin.site.register(reservas_Coworking)
admin.site.register(reservas_Coworking_provisoria)
admin.site.register(Price)
admin.site.register(Product)
admin.site.register(gallery)
admin.site.register(Wallet)
