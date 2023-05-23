from django.contrib import admin
from .models import Recipe, Rating, Review, Favorites


admin.site.register(Recipe)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Favorites)
