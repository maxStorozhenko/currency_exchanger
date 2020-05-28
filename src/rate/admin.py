from django.contrib import admin

from rate.models import Rate


class RateAdmin(admin.ModelAdmin):
    list_per_page = 19
    list_display = ('id', 'created', 'rate', 'source', 'currency_type', 'rate_type')
    fields = ('id', 'created', 'rate', 'source', 'currency_type', 'rate_type')


admin.site.register(Rate, RateAdmin)
