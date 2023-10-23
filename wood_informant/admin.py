from django.contrib import admin

from .models import Actual, Previous, Profile, Message
from .forms import ProfileForm

PRICE_FILTER_STEPS = 10

class PriceFilter(admin.SimpleListFilter):
    title = 'Цена'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        # Вытащить полный список цен
        prices = [c.price for c in model_admin.model.objects.all()]
        prices = list(filter(None, prices))
        if not prices:
            return

        # TODO: найти "кластера цен", то есть такие интервалы, внутри которых точно есть продукты!

        # Побить его на 10 интервалов
        max_price = max(prices)
        chunk = int(max_price / PRICE_FILTER_STEPS)
        print(f'max_price = {max_price}, chunk = {chunk}')

        intervals = [
            (f'{chunk * i},{chunk * (i + 1)}', f'{chunk * i} - {chunk * (i + 1)}')
            for i in range(PRICE_FILTER_STEPS)
        ]
        return intervals

    def queryset(self, request, queryset):
        choice = self.value() or ''
        if not choice:
            return queryset
        choice = choice.split(',')
        if not len(choice) == 2:
            return queryset
        price_from, price_to = choice
        return queryset.distinct().filter(price__gte=price_from, price__lt=price_to)

@admin.register(Actual)
class ActualAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Actual._meta.get_fields()]
    list_filter = ('status', 'product', 'post_date', PriceFilter, 'parse_date')

@admin.register(Previous)
class PreviousAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Previous._meta.get_fields()]
    list_filter = ('status', 'product', 'post_date', PriceFilter)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')