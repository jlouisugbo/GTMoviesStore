from django.contrib import admin
from .models import Order, Item

class ItemInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Item
    extra = 1  # Number of empty forms to show for adding new items

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'date')  # Display these in the list view
    inlines = [ItemInline]  # This links Items to Orders in admin

class ItemAdmin(admin.ModelAdmin):
    list_display = ('imdb_id', 'movie', 'price', 'quantity', 'order')

    def imdb_id(self, obj):
        return obj.movie.imdb_id

    imdb_id.admin_order_field = 'movie__imdb_id'  # Allows sorting by imdb_id
    imdb_id.short_description = 'ID'

admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)