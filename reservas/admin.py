from calendar import Calendar
from django.contrib import admin
from .models import gallery, meetingRoomCalendar, meetingRoomProvisoria, meetingRooms, mensagen, Product, reservas_Coworking, reservas_Coworking_provisoria, Price, Wallet, bundleProvisorio, transaction


class meetingRoomCalendarAdmin(admin.ModelAdmin):
    list_filter= ['date', 'startTime', 'endTime']
    list_display= ['user', 'date', 'startTime', 'endTime']
    

admin.site.register(meetingRoomCalendar, meetingRoomCalendarAdmin)

class bundleProvisorioAdmin(admin.ModelAdmin):
    search_fields=('transaction_id',)
    list_display= ['user', 'transaction_id']
    list_filter = ['bundle_5', 'bundle_10']

admin.site.register(bundleProvisorio, bundleProvisorioAdmin)

class mensagenAdmin(admin.ModelAdmin):
    search_fields=('ClientName', 'ClientEmail', 'ClientMessage')
    list_display= ['user', 'date', 'ClientName', 'Reason', 'ClientEmail', 'ClientMessage', 'Pendente']
    list_filter = ['date', 'Pendente']
    

admin.site.register(mensagen, mensagenAdmin)

class reservas_CoworkingAdmin(admin.ModelAdmin):
    list_display= ['user', 'startDate', 'endDate']
    list_filter = ['startDate', 'endDate']
    

admin.site.register(reservas_Coworking, reservas_CoworkingAdmin)
    

admin.site.register(Wallet)

class transactionAdmin(admin.ModelAdmin):
    search_fields=('transactionId',)
    list_display= ['user', 'status', 'payment_Method', 'transactionId', 'price']
    list_filter = ['status', 'payment_Method', 'price']

admin.site.register(transaction, transactionAdmin)