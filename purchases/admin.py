from django.contrib import admin

from purchases.models import Shipment, Coupon
from purchases.constants import SHIPMENT_STATUS_DELIVERED, \
    SHIPMENT_STATUS_DISPATCHED


def set_delivered(modeladmin, request, queryset):
    queryset.update(status=SHIPMENT_STATUS_DELIVERED)
set_delivered.short_description = 'Actualizar como entregado'

def set_dispatched(modeladmin, request, queryset):
    queryset.update(status=SHIPMENT_STATUS_DISPATCHED)
set_dispatched.short_description = 'Actualizar como en camino'

class ShipmentAdmin(admin.ModelAdmin):
    actions = [set_delivered, set_dispatched]
    list_filter = ('status',)
    ordering = ('individual_purchase__creation_date',)


class CouponAdmin(admin.ModelAdmin):
    pass

admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.disable_action('delete_selected')

admin.site.site_header = "módulo de administración de walen"
admin.site.site_title = "Administración de walen"
admin.site.index_title = "Bienvenido"
site_header = 'Ingresá al módulo de administración'