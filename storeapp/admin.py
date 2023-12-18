from django.contrib import admin
from .models import Categories,Author,Course,Level

admin.site.register(Categories)
admin.site.register(Course)
admin.site.register(Author)
admin.site.register(Level)
