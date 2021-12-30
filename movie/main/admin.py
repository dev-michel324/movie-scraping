from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ("nome", "link", "categoria", "added")

admin.site.register(Categoria)
