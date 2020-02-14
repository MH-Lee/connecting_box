from django.contrib import admin
from .models import EmailContents, Tag
# Register your models here.

class EmailContentsAdmin(admin.ModelAdmin):
    list_display = ('title', 'registered_dttm')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(EmailContents, EmailContentsAdmin)
admin.site.register(Tag, TagAdmin)