from django.contrib import admin
from .models import Menu, category

class MenuAdmin(admin.ModelAdmin):
    pass
    #list_display_links = ('pk',)
    #prepopulated_fields = {'slug':'name'}

class CategoryAdmin(admin.ModelAdmin):
    pass
    #list_display_links = ('pk',)
    #prepopulated_fields = {'slug':'value'}
admin.site.register(Menu,MenuAdmin)
admin.site.register(category,CategoryAdmin)
