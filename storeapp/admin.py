from django.contrib import admin
from .models import Categories,Author,Course,Level,what_will_learn,course_requirement

class what_you_learnTabularinline(admin.TabularInline):
    model=what_will_learn
    
class course_requirementTabularinline(admin.TabularInline):
    model=course_requirement
    
class course_admin(admin.ModelAdmin):
    inlines=(what_you_learnTabularinline,course_requirementTabularinline)
    
admin.site.register(Categories)
admin.site.register(Course,course_admin)
admin.site.register(Author)
admin.site.register(Level)
admin.site.register(what_will_learn)
