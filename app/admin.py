from django.contrib import admin

from .models import Producer, Device, Week, Sale, PredictedSale, Transaction, Campaign

admin.site.register(Producer),
admin.site.register(Device),
admin.site.register(Week),
admin.site.register(Sale),
admin.site.register(PredictedSale),
admin.site.register(Transaction),
admin.site.register(Campaign),