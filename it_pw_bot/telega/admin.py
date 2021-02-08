from django.contrib import admin
from .models import TGConfig, TGUserAmo, TGAmoChat, TGLogist

admin.site.register(TGConfig)

@admin.register(TGAmoChat)
class TGAmoChatAdmin(admin.ModelAdmin):
    list_display = ('amo_leads_id', 'text', 'amo2tg', 'issend', 'iserror',)


@admin.register(TGLogist)
class TGAmoChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'tg_id',)

@admin.register(TGUserAmo)
class TGUserAmoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'amo_id', 'amo_leads_id', 'tg_id', 'rating',  'active_orderbot','choice',)
    filter_horizontal = ('city', 'technique', 'district', 'choice_orderbot', 'orderbot',)
