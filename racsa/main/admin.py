from django.contrib import admin
from .models import reviews, category, user

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk','author','text')
    list_display_links = ('pk',)
    search_fields = ('author','text')

admin.site.register(reviews, ReviewsAdmin)
admin.site.register(category)
admin.site.register(user)


